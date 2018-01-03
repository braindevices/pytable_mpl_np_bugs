#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
show strange bugs of pytables import order
Created on 01/02/18-12:52 AM

@author: lingwangneuraleng@gmail.com
"""
import os, sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter


def create_demodata(dirpath, nt, nj, ni):
    import os
    import numpy as np
    import tables as pytb
    _path = os.path.join(dirpath, "test_data.h5")
    print("create {} with data shape [{}, {}, {}]".format(_path, nt, nj, ni))
    tbattrs = dict(
        nj = nj,
        ni = ni,
    )
    clib = 'blosc:lz4'
    clevel = 9
    comp_filter = pytb.Filters(complib=clib, complevel=clevel)
    data = np.random.randn(nt, nj, ni)
    h5 = pytb.open_file(_path, mode="w")
    h5.set_node_attr('/', 'params', tbattrs)
    h5data = h5.create_earray(
        '/', 'h5data',
        atom=pytb.Atom.from_dtype(data.dtype),
        shape=(0, nj, ni),
        filters=comp_filter
    )
    h5data.append(data)
    h5.close()


def import_later():
    print("import pytables after matplotlib or after numpy is OK: ")
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    print("mpl version: ", mpl.__version__, "plt with backend: ", plt.get_backend())
    import numpy as np
    import tables as pytb
    print("pytable version: ", pytb.__version__)
    print("read file")
    h5 = pytb.open_file("test_data.h5")
    h5data = h5.root.h5data
    nt, nj, ni = h5data.shape
    _data = h5.root.h5data[0]
    _data2 = h5.root.h5data[1]
    print(_data.shape)
    print("try to create fig")
    fig, ax = plt.subplots()
    arrowstride = 1
    arrowwidth = 0.001
    XI, YI = np.meshgrid(np.linspace(0, ni - 1, ni), np.linspace(0, nj - 1, nj))
    qv = ax.quiver(
        XI[::arrowstride, ::arrowstride],
        YI[::arrowstride, ::arrowstride],
        _data[::arrowstride, ::arrowstride],
        _data2[::arrowstride, ::arrowstride],
        units='width',
        angles='xy',
        scale_units='xy',
        scale=2,
        headlength=4,
        width=arrowwidth,
        headwidth=3,
        headaxislength=3,
        color='C8',
    )
    print("figure creation is OK")
    print("figure creation is OK")

def show_bug():
    import tables as pytb
    print("pytable version: ", pytb.__version__)
    print("import pytables before matplotlib and numpy causes `Segmentation fault` or `libpng error: IDAT: bad parameters to zlib`")
    import numpy as np
    print("numpy version: ", np.__version__)
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    print("mpl version: ", mpl.__version__, "plt with backend: ", plt.get_backend())
    print("read file")
    h5 = pytb.open_file("test_data.h5")
    h5data = h5.root.h5data
    nt, nj, ni = h5data.shape
    _data = h5.root.h5data[0]
    _data2 = h5.root.h5data[1]
    print(_data.shape)
    print("try to create fig")
    fig, ax = plt.subplots()
    arrowstride = 1
    arrowwidth = 0.001
    XI, YI = np.meshgrid(np.linspace(0, ni-1, ni), np.linspace(0, nj-1, nj))
    qv = ax.quiver(
        XI[::arrowstride, ::arrowstride],
        YI[::arrowstride, ::arrowstride],
        _data[::arrowstride, ::arrowstride],
        _data2[::arrowstride, ::arrowstride],
        units='width',
        angles='xy',
        scale_units='xy',
        scale=2,
        headlength=4,
        width=arrowwidth,
        headwidth=3,
        headaxislength=3,
        color='C8',
    )
    print("figure creation is OK")


def main():
    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    try:
        parser = ArgumentParser(description=program_shortdesc, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        switchgroup = parser.add_mutually_exclusive_group(required=True)
        iogroup = parser.add_argument_group()
        switchgroup.add_argument(
            "--create_data",
            dest="create_data",
            help="create test data in ./ [default: %(default)s]",
            action="store_true"
        )
        iogroup.add_argument(
            "--nt",
            dest="nt",
            help="create test data with nt frames >=2 [default: %(default)s]",
            metavar="number_of_frame",
            default=2,
            type=int,
        )
        iogroup.add_argument(
            "--nj",
            dest="nj",
            help="create test data with nj rows >=2 [default: %(default)s]",
            metavar="number_of_rows",
            default=3000,
            type=int,
        )
        iogroup.add_argument(
            "--ni",
            dest="ni",
            help="create test data with ni cols >=2 [default: %(default)s]",
            metavar="number_of_cols",
            default=4000,
            type=int,
        )
        switchgroup.add_argument(
            "--demo_bug",
            dest="demo_bug",
            help="demonstrate the bug [default: %(default)s]",
            action="store_true"
        )
        switchgroup.add_argument(
            "--demo_ok",
            dest="demo_ok",
            help="demonstrate the normal case [default: %(default)s]",
            action="store_true"
        )

        args = parser.parse_args()
        if args.create_data:
            print("data")
            nt = args.nt
            nj = args.nj
            ni = args.ni
            print("data shape = [{} {} {}]".format(nt, nj, ni))
            create_demodata("./", nt, nj, ni)
        if args.demo_bug:
            print("bug")
            show_bug()
        if args.demo_ok:
            print("OK")
            import_later()
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == '__main__':
    sys.exit(main())
