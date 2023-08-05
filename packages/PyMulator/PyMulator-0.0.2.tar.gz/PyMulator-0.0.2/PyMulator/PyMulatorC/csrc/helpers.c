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
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "interface.h"


/* what set_updatePC and _get_updatePC actually modify */
static uint8_t updatePC;

int32_t _read32 ( const char * gdb_cmd, uint32_t * val)
{
    char * cmd; 
    char * resp;
    
    //copy the const cmd into another buffer
    asprintf( &cmd, "%s", gdb_cmd);
    //callback to get data
    call_from_mulator(cmd, &resp);
    
    //parse the response data
    if (resp == NULL) goto _read32err; 

    char * arg1 = strtok(resp, " \t");
    char * arg2 = strtok(NULL, " \t");

    if (arg1 == NULL) goto _read32err;
    if (arg2 == NULL) goto _read32err; 

    //pull out the value
    *val = (uint32_t) strtol( arg2, NULL, 16); 

    //cleanup memory
    free(cmd);
    free(resp);
   
    //and we're done
    return 0;

    _read32err:
    free(cmd);
    free(resp);
    return -1;
}

int32_t _write32 ( const char * gdb_cmd, uint32_t * val)
{
    char * cmd; 
    char * resp;
    
    //copy the const cmd into another buffer
    asprintf( &cmd, "%s", gdb_cmd);
    //callback to get data
    call_from_mulator(cmd, &resp);
    
    //parse the response data
    if (resp== NULL) goto _write32err;

    char * arg1 = strtok(resp, " \t");
    //writes come with an equal sign
    strtok(NULL, " \t"); 
    char * arg2 = strtok(NULL, " \t");
    if ( arg1 == NULL) goto _write32err;
    if ( arg2 == NULL) goto _write32err;

    //pull out the value
    *val = (uint32_t) strtol( arg2, NULL, 16); 

    //cleanup memory
    free(cmd);
    free(resp);
   
    //and we're done
    return 0;

    _write32err:
    
    free(cmd);
    free(resp);
    return -1;
}

int32_t _write( const char * gdb_cmd)
{
    char * cmd; 
    char * resp = NULL;
    
    //copy the const cmd into another buffer
    asprintf( &cmd, "%s", gdb_cmd);

    //callback to get data
    call_from_mulator(cmd, &resp);

    return (strnlen(resp, 255) == 0);
}

void _set_updatePC(uint8_t _true)
{
    updatePC = _true;
}

uint8_t _get_updatePC(void)
{
    return updatePC;
}

