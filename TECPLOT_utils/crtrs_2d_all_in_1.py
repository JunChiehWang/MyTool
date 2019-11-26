#!/dat/usr/e121341/anaconda3/bin/python3

import argparse
import os
import subprocess
import datetime

version = '20190613'


##############################################################################
def getArgs(argv=None):

    # parser:
    # The The default help formatter re-wraps lines to fit your terminal
    # (it looks at the COLUMNS environment variable to determine the output
    # width, defaulting to 80 characters total).
    # Use the RawTextHelpFormatter class instead to indicate that you already
    # wrapped the lines .
    # RawTextHelpFormatter maintains whitespace for all sorts of help text,
    # including argument descriptions.
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
            description="""
    This script generates a tecplot macro file which read all crtrs 2d files
    & show them in multiple frames in 1 layout so it's easier to compare with.

    -w   = width of each frame, default = 3.35 inch
    -hei = height of each frame, default = 4 inch
    -in  = input files
    -out = output layout
           default = ./crtrs_Nd.plt.dat.lay
    -map = file of colormap to be loaded
           default =
           ~/bin/JunChieh_Wang/
           tecplot/tecplot_modified_color_map_20190502map'

           with mapname = 'modified_ranbow_1'
           if 'none', then no colormap will be loaded

    example:
    python3 crtrs_2d_all_in_1.py -in ./*/2d.plt.dat -out ./2d.plt.dat.lay
    python3 crtrs_2d_all_in_1.py -w 4 -h 7 -in ./*25mt*/crtrs_2d.plt.dat

    """, formatter_class=argparse.RawTextHelpFormatter)

    #
    # positional argument
    #

    #
    # optional argument
    #
    parser.add_argument(
            "-v", "--version", action="version",
            version="version: " + str(version))
    parser.add_argument("-w", "--width", help="width of each frame (inch)")
    parser.add_argument("-hei", "--height", help="height of each frame (inch)")
    parser.add_argument(
            "-in", "--input_file", nargs='*',
            help="input files to be plotted")
    parser.add_argument("-out", "--output_layout", help="output layout")
    parser.add_argument("-map", "--colormap", help="colormap file")

    args = parser.parse_args()

    # current directory
    current_dir = os.getcwd()
#
    if args.width:
        width = float(args.width)
        print('\nwidth of each frame: {} inch'.format(width))
    else:
        width = float(3.35)
        print('\nwidth is not specified from command-line')
        print('set width to : {} inch'.format(width))
#
    if args.height:
        height = float(args.height)
        print('\nheight of each frame: {} inch'.format(height))
    else:
        height = float(4)
        print('\nheight is not specified from command-line')
        print('set height to : {} inch'.format(height))
#
    if args.input_file:
        input_file = args.input_file
        print('\ninput files to be included:')
        for inf in input_file:
            print(inf)
    else:
        print("\ninput files are not specified, script exits!")
        exit()
#
    if args.output_layout:
        output_layout = str(args.output_layout)
        print('\noutput_layout: {}'.format(output_layout))
    else:
        # date and time
        date = datetime.datetime.now()
        date = '{}{}{}'.format(date.year, date.month, date.day)
        output_layout = './crtrs_Nd_{}.plt.dat.lay'.format(date)
        print('\noutput_layout is not specified from command-line')
        print('set output_layout to : {}'.format(output_layout))
#
    if args.colormap:
        if (args.colormap == 'none'):
            print('\ncolormap will not be loaded')
            colormap = None
        else:
            colormap = str(args.colormap)
            print('\ncolormap file from: {}'.format(colormap))
    else:
        colormap = '~/bin/JunChieh_Wang/tecplot/' \
                   'tecplot_modified_color_map_20190502.map'
        print('\ncolormap file is not specified from command-line')
        print('set colormap to : {}'.format(colormap))

    return width, height, input_file, output_layout, colormap


###############################################################################
def crtrs_Nd_all_in_1(width, height, input_file, output_layout, colormap):

    # check if output_layout exist
    output_layout_path = os.path.realpath(output_layout)
    if not os.path.isfile(output_layout_path):
        print('\ncreate output_layout: {}'.format(output_layout_path))
    else:
        print('\noutput_layout exist: {}'.format(output_layout_path))
        overwrite = input('overwrite the file ? (yes or no) ')
        overwrite = overwrite.strip().lower()
        if overwrite == 'yes':
            print('overwrite it !')
        elif overwrite == 'no':
            print('not overwrite it, script exits!')
            exit()

    # create macro for tecplot
    macro_name = '2d_plot.mcr'
    with open(macro_name, 'w') as m:

        # write head line
        line = '#!MC 1410\n'
        m.write(line)

        # check if color map exist, and load color map file
        if colormap is not None:
            colormap_path = os.path.realpath(os.path.expanduser(colormap))
            if os.path.isfile(colormap_path):
                line = '$!LoadColorMap  \"{}\"'.format(colormap_path)
                m.write(line)
            else:
                print('\ncolormap does not exist!')
                print('check the path:{}'.format(colormap_path))

        # build block for each frame
        for count, f in enumerate(input_file, 0):

            # find and file and check is it exist
            file_name = f.split('./')[1]
            file_path = os.path.realpath(file_name)
            if os.path.isfile(file_path):
                print('\nworking on file {}'.format(file_path))
            else:
                print('\nfile not found {}'.format(file_path))

            # need double {{ and }} for curly-brace characters in python
            line = """
            $!CreateNewFrame
                XYPos
                    {{
                    X = {}
                    Y = {}
                    }}
                Width = {}
                Height = {}
            $!FrameLayout ShowBorder = Yes
            $!FrameName = \'{}\'
            $!ReadDataSet  \'\"{}\" \'
                ReadDataOption = New
                ResetStyle = Yes
                VarLoadMode = ByName
                AssignStrandIDs = Yes
                VarNameList = ''
            $!RenameDataSetZone
                Zone = 1
                Name = \'{}\'
            $!FieldLayers ShowShade = No
            $!FieldLayers ShowContour = Yes
            $!FieldLayers ShowEdge = Yes
            $!FrameLayout ShowBorder = No
            $!TwoDAxis ViewportPosition{{X1 = 1}}
            $!TwoDAxis ViewportPosition{{X2 = 99}}
            $!TwoDAxis ViewportPosition{{Y2 = 99}}
            $!TwoDAxis ViewportPosition{{Y1 = 1}}
            $!TwoDAxis XDetail{{Ticks{{ShowOnAxisLine = No}}}}
            $!TwoDAxis YDetail{{Ticks{{ShowOnAxisLine = No}}}}
            $!TwoDAxis XDetail{{TickLabel{{ShowOnAxisLine = No}}}}
            $!TwoDAxis YDetail{{TickLabel{{ShowOnAxisLine = No}}}}
            $!TwoDAxis XDetail{{Title{{ShowOnAxisLine = No}}}}
            $!TwoDAxis YDetail{{Title{{ShowOnAxisLine = No}}}}
            $!TwoDAxis XDetail{{AxisLine{{Show = No}}}}
            $!TwoDAxis YDetail{{AxisLine{{Show = No}}}}
            $!TwoDAxis XDetail{{ShowAxis = No}}
            $!TwoDAxis YDetail{{ShowAxis = No}}
            $!FieldMap [1]  Contour{{ContourType = BothLinesAndFlood}}
            $!FieldMap [1]  Contour{{Color = Black}}
            $!FieldMap [1]  Contour{{LineThickness = 0.02}}
            """.format(
                    count*width, 0, width, height, file_name, file_name,
                    file_name
                    )
            m.write(line)

            # add file_name to the plot
            line = """
            $!AttachText
                AnchorPos
                    {{
                    X = {}
                    Y = {}
                    }}
                TextShape
                    {{
                    IsBold = Yes
                    SizeUnits = Frame
                    Height = 3
                    }}
                Text = \'{}\'
            """.format(0, 90, file_name)
            m.write(line)

            # select colormap
            if colormap is not None:
                if os.path.isfile(colormap):
                    line = '$!GlobalContour 1  ColorMapName = \'{}\''.        \
                            format('modified_ranbow_1')
                    m.write(line)

        # remove the default frame
        line = """
        $!Pick AddAtPosition
            X = 10.0274725275
            Y = 8.19139194139
            ConsiderStyle = Yes
        $!FrameControl ActivateByNumber
            Frame = 1
        $!FrameControl DeleteTop
        """
        m.write(line)

        # link frames
        line = """
        $!Linking BetweenFrames{LinkSolutionTime = Yes}
        $!Linking BetweenFrames{LinkXAxisRange = Yes}
        $!Linking BetweenFrames{LinkYAxisRange = Yes}
        $!Linking BetweenFrames{LinkAxisPosition = Yes}
        $!Linking BetweenFrames{LinkValueBlanking = Yes}
        $!Linking BetweenFrames{LinkContourLevels = Yes}
        $!PropagateLinking
            LinkType = BetweenFrames
            FrameCollection = All
        $!Linking WithinFrame{LinkAxisStyle = Yes}
        $!Linking WithinFrame{LinkGridlineStyle = Yes}
        $!Linking WithinFrame{LinkLayerLineColor = Yes}
        $!Linking WithinFrame{LinkLayerLinePattern = Yes}
        $!PropagateLinking
            LinkType = WithinFrame
            FrameCollection = All
        """
        m.write(line)

        # save the layout file
        line = '\n$!SaveLayout  \"{}\"\n'.format(output_layout)
        line = line + 'UseRelativePaths = Yes'
        m.write(line)
        m.close()

    # execute the macro
    subprocess.Popen(['tec360', '-quiet', '-b', '-p', macro_name])
    # subprocess.Popen(['tec360', '-b', '-p', macro_name])


###############################################################################
#
###############################################################################
def main():
    width, height, input_file, output_layout, colormap = getArgs()
    crtrs_Nd_all_in_1(
            width=width, height=height, input_file=input_file,
            output_layout=output_layout, colormap=colormap
            )


###############################################################################
#
###############################################################################
if __name__ == '__main__':
    main()
