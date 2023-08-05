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

#include "cpu/core.h"

#include "helpers.h"

uint32_t 
read_word_quiet(uint32_t addr)
{
    return read_word(addr);
}

uint32_t 
read_word(uint32_t addr)
{
    char buf [255];
    snprintf( (char*)&buf, 255, "x/1xw 0x%x", addr);
    uint32_t val;

    if ( _read32(buf, &val) < 0){
        CORE_WARN("FAILED\n");
    }

    DBG2("reading word: 0x%x -> 0x%x\n", addr, val);
    return (uint16_t) val;
}

void 
write_word(uint32_t addr, uint32_t val)
{
    DBG2("writing word: 0x%x -> 0x%x\n", addr, val);

    char buf [255];
    snprintf( (char*)&buf, 255, "set {uint32_t} 0x%x = 0x%x", addr, val);
    
    _write(buf); 
}

void 
write_word_aligned(uint32_t addr, uint32_t val)
{	
    write_word(addr,val);
}

void 
write_word_unaligned(uint32_t addr, uint32_t val)
{
    DBG2("write unaligned word: 0x%x -> 0x%x\n", addr, val);
    
    uint32_t baddr = addr;
    uint8_t bval = val & 0xff;
    val = val >> 8;
    for (int i = 0; i < 4; ++i){
        write_byte(baddr, bval);

        baddr += 1;
        bval = val & 0xff;
        val = val >> 8;
    }
}

uint16_t 
read_halfword(uint32_t addr)
{
    char buf [255];
    snprintf( (char*)&buf, 255, "x/1xh 0x%x", addr);
    uint32_t val;

    if ( _read32(buf, &val) < 0){
        CORE_WARN("FAILED\n");
    }

    assert(  (val & 0xffff0000) == 0 ); //make sure it's only a half-word

    DBG2("reading halfword: 0x%x -> 0x%x\n", addr, val);
    return (uint16_t) val;
}

void 
write_halfword(uint32_t addr, uint16_t val)
{
    DBG2("writing halfword: 0x%x -> 0x%x\n", addr, val);

    char buf [255];
    snprintf( (char*)&buf, 255, "set {uint16_t} 0x%x = 0x%x", addr, val);

    _write(buf);

}

void 
write_halfword_unaligned(uint32_t addr, uint16_t val)
{

    DBG2("writing halfword: 0x%x -> 0x%x\n", addr, val);

    uint32_t baddr = addr;
    uint8_t bval = val & 0xff;
    val = val >> 8;
    for (int i = 0; i < 2; ++i){
        write_byte(baddr, bval);

        baddr += 1;
        bval = val & 0xff;
        val = val >> 8;
    }
}

uint8_t 
read_byte(uint32_t addr)
{
    char buf [255];
    snprintf( (char*)&buf, 255, "x/1xb 0x%x", addr);
    uint32_t val;

    if ( _read32(buf, &val) < 0){
        CORE_WARN("FAILED\n");
    }

    assert( val <= 0xff ); //make sure it's only a byte

    DBG2("reading byte: 0x%x -> 0x%x\n", addr, val);
    return (uint8_t) val;

}

void 
write_byte(uint32_t addr, uint8_t val)
{
    DBG2("writing byte: 0x%x -> 0x%x\n", addr, val);

    char buf [255];
    snprintf( (char*)&buf, 255, "set {uint8_t} 0x%x = 0x%x", addr, val);

    _write(buf);


}


