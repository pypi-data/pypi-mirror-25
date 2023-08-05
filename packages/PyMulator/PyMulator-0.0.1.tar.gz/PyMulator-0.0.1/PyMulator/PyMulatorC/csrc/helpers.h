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
#ifndef __HELPERS_H__
#define __HELPERS_H__

#include <stdlib.h>
#include <stdint.h>

/**
 * calls the host callback with a read gdb-like command
 * (ie you want to read data from the host)
 * and parses the result as a 32-bit int
 * @param gdb_cmd the gdb-like command
 * @param val pointer to where the parsed 32-bit int will be returned
 * @return 0: success, <0: failure
 */
int32_t _read32 ( const char * gdb_cmd, uint32_t * val );

/**
 * calls the host callback with a write gdb-like command
 * (ie you want to write data to the host)
 * and parses the result as a 32-bit int
 * @param gdb_cmd the gdb-like command
 * @param val pointer to where the parsed 32-bit result will be returned
 * @return 0: success, <0: failure
 */
int32_t _write32 ( const char * gdb_cmd, uint32_t * val );

/**
 * calls the host callback with a write gdb-like command
 * (ie you want to write data to the host)
 * and parses the result as a 32-bit int
 * @param gdb_cmd the gdb-like command
 * @param val pointer to where the parsed 32-bit result will be returned
 * @return 0: success, <0: failure
 */
int32_t _write ( const char * gdb_cmd );


/** 
 * a way to let PyMulator know that the PC has been updated
 * @param _true: set to false before the instruction, 
 *              and CORE_reg_write() will set to true if PC is written
 */
void   _set_updatePC(uint8_t _true);

/**
 * a way to let PyMulator know that the PC has been updated
 * @return true if CORE_reg_write() has written the PC
 */
uint8_t _get_updatePC(void);


#if __STDC_VERSION__ < 199901L
     # if __GNUC__ >= 2
         #  define __func__ __FUNCTION__
     # else
         #  define __func__ "<unknown>"
     # endif
#endif

/**
 * Defines what to do for unimplimented functions
 * Prints out where it's not implimented, then terminates
 */
#define UNIMPLIMENTED()                                 \
    do {                                                \
        fprintf(stderr, "%s:%d:%s NOT IMPLIMENTED\n",   \
                __FILE__, __LINE__, __func__);          \
        exit(EXIT_FAILURE);                             \
    } while(0)              

#endif


