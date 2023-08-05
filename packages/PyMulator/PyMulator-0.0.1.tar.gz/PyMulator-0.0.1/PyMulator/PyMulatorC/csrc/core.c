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

/**
 * called for an illegal instruction
 */
void 
CORE_ERR_illegal_instr_real( const char * f, int l, uint32_t inst)
{
    printf("CORE_ERR_illegal_instr, inst: %08x\n", inst);
    printf("Dumping core...\n");
    printf( "%s:%d\tUnknown inst\n", f, l);
    exit(EXIT_FAILURE);
}

/**
 * called for an un-implimented instruction
 */
void 
CORE_ERR_not_implemented_real(const char *f, int l, const char *opt_msg) {
    printf("%s:%d\tCORE_ERR_not_implemented -- %s\n", f, l, opt_msg);
    exit(EXIT_FAILURE);
}

/** 
 * called for ARM's "UNPREDICTABLE" instructions
 */
void 
CORE_ERR_unpredictable_real(const char *f, int l, const char *opt_msg) {
    printf( "%s:%d\tCORE_ERR_unpredictable -- %s\n", f, l, opt_msg);
    exit(EXIT_FAILURE);
}


