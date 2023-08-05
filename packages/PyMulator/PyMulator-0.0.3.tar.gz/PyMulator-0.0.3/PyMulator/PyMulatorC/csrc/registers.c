/* Mulator - An extensible {ARM} {e,si}mulator
 * Copyright 2011-2012  Pat Pannuto <pat.pannuto@gmail.com>
 * Copyright 2017  Andrew Lukefahr <lukefahr@indiana.edu>
 *
 * This file is part of Mulator.
 *
 * Mulator is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Mulator is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Mulator.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <assert.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "core/common.h"
#include "core/pipeline.h"
#include "cpu/registers.h"

#include "helpers.h"
#include "interface.h"

#ifndef M_PROFILE
    #error "Only supports M_PROFILE currently"
#endif

enum Mode CurrentMode;

uint32_t physical_primask;
//     0: priority	The exception mask register, a 1-bit register.
//			Setting PRIMASK to 1 raises the execution priority to 0.
uint32_t physical_basepri;
/* The base priority mask, an 8-bit register. BASEPRI changes the priority
 * level required for exception preemption. It has an effect only when BASEPRI
 * has a lower value than the unmasked priority level of the currently
 * executing software.  The number of implemented bits in BASEPRI is the same
 * as the number of implemented bits in each field of the priority registers,
 * and BASEPRI has the same format as those fields.  For more information see
 * Maximum supported priority value on page B1-636.  A value of zero disables
 * masking by BASEPRI.
 */
uint32_t physical_faultmask;
/* The fault mask, a 1-bit register. Setting FAULTMASK to 1 raises the
 * execution priority to -1, the priority of HardFault. Only privileged
 * software executing at a priority below -1 can set FAULTMASK to 1. This means
 * HardFault and NMI handlers cannot set FAULTMASK to 1. Returning from any
 * exception except NMI clears FAULTMASK to 0.
 */

union control_t physical_control;
//     0: nPRIV, thread mode only (0 == privileged, 1 == unprivileged)
//     1: SPSEL, thread mode only (0 == use SP_main, 1 == use SP_process)
//     2: FPCA, (1 if FP extension active)



////////////////////////////////////////////////////////////////////////////////

uint32_t CORE_reg_read(int r)
{
    uint32_t val = -1;  
    char buf [255];

    if (r == SP_REG) {
        snprintf( (char*)&buf, 255, "info register sp");
	} else if (r == LR_REG) {
        snprintf( (char*)&buf, 255, "info register lr");
	} else if (r == PC_REG) {
        snprintf( (char*)&buf, 255, "info register pc");
	} else if (r >= 0 && r <= 12){
        snprintf( (char*)&buf, 255, "info register r%d", r);
    } else {
        UNIMPLIMENTED();
    }

    if ( _read32(buf, &val) < 0){
        CORE_WARN("FAILED\n");
    }

    DBG2("reading reg: %d -> 0x%x\n", r, val);
    return val;
       
}

void CORE_reg_write(int r, uint32_t val) 
{
    char buf [255];

    if (r == SP_REG) {
        snprintf( (char*)&buf, 255, "p $sp = 0x%x", val); 
	} else if (r == LR_REG) {
        snprintf( (char*)&buf, 255, "p $lr = 0x%x", val); 
	} else if (r == PC_REG) {
        snprintf( (char*)&buf, 255, "p $pc = 0x%x", val); 

        #ifdef NO_PIPELINE
                pipeline_flush_exception_handler(val & 0xfffffffe);
                //hack-ish
                _set_updatePC(true);
        #else
            #error "What to do here?"
        #endif

	} else if (r >= 0 && r <= 12){
        snprintf( (char*)&buf, 255, "p $r%d = 0x%x", r, val); 
    } else {
        UNIMPLIMENTED();
    }

    uint32_t ret;
    if (_write32(buf, &ret) < 0){
        CORE_WARN("FAILED\n");
    }

    assert(ret == val);

    DBG2("writing reg: %d -> 0x%x\n", r, val);
     
	//	pipeline_flush_exception_handler(val & 0xfffffffe);

}

// <8:0> from IPSR
// <26:24,15:10> from ESPR
// <31:27>,[if DSP: <19:16>] from APSR
static const uint32_t xPSR_ipsr_mask = 0x000001ff;
static const uint32_t xPSR_epsr_mask = 0x0700fc00;
//static const uint32_t xPSR_apsr_dsp_mask = 0xf80f0000;
static const uint32_t xPSR_apsr_nodsp_mask = 0xf8000000;

uint32_t CORE_xPSR_read(void) {
    const char * xpsr_rd= "info register xpsr";
    uint32_t xpsr;
    if ( _read32(xpsr_rd, &xpsr) < 0){
        CORE_WARN("FAILED\n");
    }

    DBG2("reading reg: xpsr -> 0x%x\n", xpsr);
    return xpsr;
}

void CORE_xPSR_write(uint32_t xPSR) {

    char buf [255];
    snprintf( (char*)&buf, 255, "p $xpsr = 0x%x", xPSR); 
    uint32_t ret;
    
    if (_write32(buf, &ret) < 0){
        CORE_WARN("reg_write FAILED\n");
    }

    assert(ret == xPSR);
    DBG2("Writing xpsr: %x\n", xPSR);

}

enum Mode CORE_CurrentMode_read(void) {
    enum Mode cur;
    cur = Mode_Thread;
    return cur;
}

void CORE_CurrentMode_write(enum Mode mode) {
    if (mode == Mode_Thread){
        DBG2("Setting Mode to thread\n");
    } else{
        DBG2("Setting Mode to Handler?\n");
        assert(false);
        UNIMPLIMENTED();
    }
}

union apsr_t CORE_apsr_read(void) {

    uint32_t xpsr = CORE_xPSR_read();

	union apsr_t apsr;
    apsr.storage = xpsr & xPSR_apsr_nodsp_mask;

    DBG2("reading reg: apsr-> 0x%x\n", apsr.storage);

    return apsr;
}



void CORE_apsr_write(union apsr_t val) {

    const uint32_t not_apsr_mask = ~xPSR_apsr_nodsp_mask;

	if (val.storage & not_apsr_mask) {
		DBG1("WARN update of reserved APSR bits\n");
        assert(false);
	}

    //get full xpsr
    uint32_t xpsr = CORE_xPSR_read();

    //clear apsr bits
    xpsr = xpsr & (not_apsr_mask);
    //or in the new apsr bits
    xpsr = xpsr | val.storage;

    CORE_xPSR_write(xpsr);

    DBG2("writing reg: apsr-> 0x%x\n", val.storage);

}

union ipsr_t CORE_ipsr_read(void) {

    uint32_t xpsr = CORE_xPSR_read();

	union ipsr_t ipsr;
    ipsr.storage = xpsr & xPSR_ipsr_mask;

    DBG2("reading reg: ipsr-> 0x%x\n", ipsr.storage);

    return ipsr;
}

void CORE_ipsr_write(union ipsr_t val) {

	if (val.storage & ~xPSR_ipsr_mask) {
		DBG1("WARN update of reserved iPSR bits\n");
        assert(false);
	}

    //get full xpsr
    uint32_t xpsr = CORE_xPSR_read();

    //clear apsr bits
    xpsr = xpsr & (~xPSR_ipsr_mask);
    //or in the new ipsr bits
    xpsr = xpsr | val.storage;

    CORE_xPSR_write(xpsr);

    DBG2("writing reg: ipsr-> 0x%x\n", val.storage);
}

union epsr_t CORE_epsr_read(void) {

    uint32_t xpsr = CORE_xPSR_read();

	union epsr_t epsr;
    epsr.storage = xpsr & xPSR_epsr_mask;

    DBG2("reading reg: epsr-> 0x%x\n", epsr.storage);

    return epsr;
}

void CORE_epsr_write(union epsr_t val) {

	if (val.storage & ~xPSR_epsr_mask) {
		DBG1("WARN update of reserved epsr bits\n");
        assert(false);
	}

    //get full xpsr
    uint32_t xpsr = CORE_xPSR_read();

    //clear apsr bits
    xpsr = xpsr & (~xPSR_epsr_mask);
    //or in the new epsr bits
    xpsr = xpsr | val.storage;

    CORE_xPSR_write(xpsr);

    DBG2("writing reg: epsr-> 0x%x\n", val.storage);

}

bool CORE_control_nPRIV_read(void) {
    assert(false);
    UNIMPLIMENTED();
    return false;
}

void CORE_control_nPRIV_write(bool npriv) {
    assert(false);
    UNIMPLIMENTED();
}

bool CORE_control_SPSEL_read(void) {
    assert(false);
    UNIMPLIMENTED();
    return false;
}


void CORE_control_SPSEL_write(bool spsel) {
    assert(false);
    UNIMPLIMENTED();
}

void CORE_update_mode_and_SPSEL(enum Mode mode, bool spsel) {
    assert(false);
    UNIMPLIMENTED();
}

bool CORE_primask_read(void) {
    assert(false);
    UNIMPLIMENTED();
    return false;
}

void CORE_primask_write(bool val) {
    assert(false);
    UNIMPLIMENTED();
}

uint8_t CORE_basepri_read(void) {
    assert(false);
    UNIMPLIMENTED();
    return 0;
}

void CORE_basepri_write(uint8_t val) {
    assert(false);
    UNIMPLIMENTED();
}

bool CORE_faultmask_read(void) {
    assert(false);
    UNIMPLIMENTED();
    return 0;
}

void CORE_faultmask_write(bool val) {
    assert(false);
    UNIMPLIMENTED();
}

union ufsr_t CORE_ufsr_read(void) {
    assert(false);
    UNIMPLIMENTED();
	union ufsr_t u;
	return u;
}

void CORE_ufsr_write(union ufsr_t u) {
    assert(false);
    UNIMPLIMENTED();
}



