#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      v.example
# AUTHOR(S):   {NAME}

# PURPOSE:     {SHORT DESCRIPTION}
# COPYRIGHT:   (C) {YEAR} by mundialis GmbH & Co. KG and the GRASS Development Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#############################################################################

# %Module
# % description: {SHORT DESCRIPTION}.
# % keyword: vector
# % keyword: grid
# %end

# %option G_OPT_V_OUTPUT
# % key: output
# % required: yes
# % description: Base name for tiles.
# %end

# %option
# % key: box
# % required: yes
# % multiple: yes
# % description: Width and height of boxes in grid
# %end

# %option
# % key: polygon_aoi
# % required: no
# % description: Polygon to extract grid-tiles for
# %end

# import needed libraries
import atexit
import os
import grass.script as grass

# initialize global variables
rm_vec = []

# cleanup function (can be extended)
def cleanup():
    nuldev = open(os.devnull, "w")
    kwargs = {"flags": "f", "quiet": True, "stderr": nuldev}
    for rmvec in rm_vec:
        if grass.find_file(name=rmvec, element="vector")["file"]:
            grass.run_command("g.remove",
                              type="vector",
                              name=rmvec,
                              **kwargs)


def main():
    global rm_vec

    pid = os.getpid()

    # set grid
    out_grid = f"kacheln_{pid}"
    rm_vec.append(out_grid)
    grass.run_command("v.mkgrid",
                      map=out_grid,
                      position='region',
                      box=options['box'],
                      quiet=True)
    # extract only polygon_aoi area if given:
    if options['polygon_aoi']:
        out_overlay = f"overlay_aoi_grid_{pid}"
        rm_vec.append(out_overlay)
        grass.run_command("v.overlay",
                          ainput=out_grid,
                          binput=options['polygon_aoi'],
                          operator='and',
                          output=out_overlay)
    else:
        out_overlay = out_grid
    # divide into tiles
    kachel_num = grass.parse_command("v.db.select",
                                     map=out_overlay,
                                     columns='cat',
                                     flags='c',
                                     quiet=True)
    for kachel in kachel_num:
        grass.run_command("v.extract",
                          input=out_overlay,
                          output=f"{options['output']}_{kachel}",
                          cats=kachel,
                          quiet=True)
    grass.message(_(f"Created {len(kachel_num)} tiles."))


if __name__ == "__main__":
    options, flags = grass.parser()
    atexit.register(cleanup)
    main()
