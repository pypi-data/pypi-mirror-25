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
#include "core/opcodes.h"
#include "cpu/registers.h"

#include "helpers.h"

int _stepi(void);

/** this will use gdb syntax */
int call_to_mulator( const char * cmd)
{
    if( !strncmp(cmd, "stepi", sizeof("stepi")) ){
        return _stepi();
    } else{
        printf("Unrecognized command\n");
        return -1;
    }
}




int _stepi(void)
{
    uint32_t pc = CORE_reg_read( PC_REG );     
    //ARM's pc = pc + 4 (reads only, so wierd)
    pc -= 4;
    uint32_t inst = read_halfword(pc);
    
    _set_updatePC(false);
    
    // If inst[15:11] are any of
    // 11101, 11110, or 11111 then this is
    // a 32-bit thumb inst
    switch (inst & 0xf800) {
        case 0xe800:
        case 0xf000:
        case 0xf800:
        {
            inst <<= 16;
            pc = pc + 2;
            inst |= read_halfword(pc);

            break;
        }
        default:
            break;
    }
    
    struct op* op = find_op( inst);
    
    assert(op);
    if (op->is16)
        op->op16.fn(inst);
    else
        op->op32.fn(inst);

    //hack-ish
    if (!_get_updatePC()){
        //and manually adjust the PC if necessary
        DBG2("stepi: advancing pc\n");
        uint32_t npc = pc + 2;
        CORE_reg_write(PC_REG, npc);
    }
    
    return 0;
}

