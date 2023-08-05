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

#include "helpers.h"

void state_write( uint32_t *loc, uint32_t val)
{
    UNIMPLIMENTED();
}

void state_write_p (uint32_t **ploc, uint32_t *pval)
{
    UNIMPLIMENTED();
}

void state_start_tick(void)
{
    return;
}

void state_tock(void)
{
    return;
}
