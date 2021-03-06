def all_colours():
    colours = {
        "indianred":(0.8039,0.3608,0.3608,1),
        "lightcoral":(0.9412,0.502,0.502,1),
        "salmon":(0.9804,0.502,0.4471,1),
        "darksalmon":(0.9137,0.5882,0.4784,1),
        "lightsalmon":(1,0.6275,0.4784,1),
        "crimson":(0.8627,0.0784,0.2353,1),
        "red":(1,0,0,1),
        "firebrick":(0.698,0.1333,0.1333,1),
        "darkred":(0.5451,0,0,1),
        "pink":(1,0.7529,0.7961,1),
        "lightpink":(1,0.7137,0.7569,1),
        "hotpink":(1,0.4118,0.7059,1),
        "deeppink":(1,0.0784,0.5765,1),
        "mediumvioletred":(0.7804,0.0824,0.5216,1),
        "palevioletred":(0.8588,0.4392,0.5765,1),
        "lightsalmon":(1,0.6275,0.4784,1),
        "coral":(1,0.498,0.3137,1),
        "tomato":(1,0.3882,0.2784,1),
        "orangered":(1,0.2706,0,1),
        "darkorange":(1,0.549,0,1),
        "orange":(1,0.6471,0,1),
        "gold":(1,0.8431,0,1),
        "yellow":(1,1,0,1),
        "lightyellow":(1,1,0.8784,1),
        "lemonchiffon":(1,0.9804,0.8039,1),
        "lightgoldenrodyellow":(0.9804,0.9804,0.8235,1),
        "papayawhip":(1,0.9373,0.8353,1),
        "moccasin":(1,0.8941,0.7098,1),
        "peachpuff":(1,0.8549,0.7255,1),
        "palegoldenrod":(0.9333,0.9098,0.6667,1),
        "khaki":(0.9412,0.902,0.549,1),
        "darkkhaki":(0.7412,0.7176,0.4196,1),
        "lavender":(0.902,0.902,0.9804,1),
        "thistle":(0.8471,0.749,0.8471,1),
        "plum":(0.8667,0.6275,0.8667,1),
        "violet":(0.9333,0.5098,0.9333,1),
        "orchid":(0.8549,0.4392,0.8392,1),
        "fuchsia":(1,0,1,1),
        "magenta":(1,0,1,1),
        "mediumorchid":(0.7294,0.3333,0.8275,1),
        "mediumpurple":(0.5765,0.4392,0.8588,1),
        "rebeccapurple":(0.4,0.2,0.6,1),
        "blueviolet":(0.5412,0.1686,0.8863,1),
        "darkviolet":(0.5804,0,0.8275,1),
        "darkorchid":(0.6,0.1961,0.8,1),
        "darkmagenta":(0.5451,0,0.5451,1),
        "purple":(0.502,0,0.502,1),
        "indigo":(0.2941,0,0.5098,1),
        "slateblue":(0.4157,0.3529,0.8039,1),
        "darkslateblue":(0.2824,0.2392,0.5451,1),
        "mediumslateblue":(0.4824,0.4078,0.9333,1),
        "greenyellow":(0.6784,1,0.1843,1),
        "chartreuse":(0.498,1,0,1),
        "lawngreen":(0.4863,0.9882,0,1),
        "lime":(0,1,0,1),
        "limegreen":(0.1961,0.8039,0.1961,1),
        "palegreen":(0.5961,0.9843,0.5961,1),
        "lightgreen":(0.5647,0.9333,0.5647,1),
        "mediumspringgreen":(0,0.9804,0.6039,1),
        "springgreen":(0,1,0.498,1),
        "mediumseagreen":(0.2353,0.702,0.4431,1),
        "seagreen":(0.1804,0.5451,0.3412,1),
        "forestgreen":(0.1333,0.5451,0.1333,1),
        "green":(0,0.502,0,1),
        "darkgreen":(0,0.3922,0,1),
        "yellowgreen":(0.6039,0.8039,0.1961,1),
        "olivedrab":(0.4196,0.5569,0.1373,1),
        "olive":(0.502,0.502,0,1),
        "darkolivegreen":(0.3333,0.4196,0.1843,1),
        "mediumaquamarine":(0.4,0.8039,0.6667,1),
        "darkseagreen":(0.5608,0.7373,0.5451,1),
        "lightseagreen":(0.1255,0.698,0.6667,1),
        "darkcyan":(0,0.5451,0.5451,1),
        "teal":(0,0.502,0.502,1),
        "aqua":(0,1,1,1),
        "cyan":(0,1,1,1),
        "lightcyan":(0.8784,1,1,1),
        "paleturquoise":(0.6863,0.9333,0.9333,1),
        "aquamarine":(0.498,1,0.8314,1),
        "turquoise":(0.251,0.8784,0.8157,1),
        "mediumturquoise":(0.2824,0.8196,0.8,1),
        "darkturquoise":(0,0.8078,0.8196,1),
        "cadetblue":(0.3725,0.6196,0.6275,1),
        "steelblue":(0.2745,0.5098,0.7059,1),
        "lightsteelblue":(0.6902,0.7686,0.8706,1),
        "powderblue":(0.6902,0.8784,0.902,1),
        "lightblue":(0.6784,0.8471,0.902,1),
        "skyblue":(0.5294,0.8078,0.9216,1),
        "lightskyblue":(0.5294,0.8078,0.9804,1),
        "deepskyblue":(0,0.749,1,1),
        "dodgerblue":(0.1176,0.5647,1,1),
        "cornflowerblue":(0.3922,0.5843,0.9294,1),
        "mediumslateblue":(0.4824,0.4078,0.9333,1),
        "royalblue":(0.2549,0.4118,0.8824,1),
        "blue":(0,0,1,1),
        "mediumblue":(0,0,0.8039,1),
        "darkblue":(0,0,0.5451,1),
        "navy":(0,0,0.502,1),
        "midnightblue":(0.098,0.098,0.4392,1),
        "cornsilk":(1,0.9725,0.8627,1),
        "blanchedalmond":(1,0.9216,0.8039,1),
        "bisque":(1,0.8941,0.7686,1),
        "navajowhite":(1,0.8706,0.6784,1),
        "wheat":(0.9608,0.8706,0.702,1),
        "burlywood":(0.8706,0.7216,0.5294,1),
        "tan":(0.8235,0.7059,0.549,1),
        "rosybrown":(0.7373,0.5608,0.5608,1),
        "sandybrown":(0.9569,0.6431,0.3765,1),
        "goldenrod":(0.8549,0.6471,0.1255,1),
        "darkgoldenrod":(0.7216,0.5255,0.0431,1),
        "peru":(0.8039,0.5216,0.2471,1),
        "chocolate":(0.8235,0.4118,0.1176,1),
        "saddlebrown":(0.5451,0.2706,0.0745,1),
        "sienna":(0.6275,0.3216,0.1765,1),
        "brown":(0.6471,0.1647,0.1647,1),
        "maroon":(0.502,0,0,1),
        "white":(1,1,1,1),
        "snow":(1,0.9804,0.9804,1),
        "honeydew":(0.9412,1,0.9412,1),
        "mintcream":(0.9608,1,0.9804,1),
        "azure":(0.9412,1,1,1),
        "aliceblue":(0.9412,0.9725,1,1),
        "ghostwhite":(0.9725,0.9725,1,1),
        "whitesmoke":(0.9608,0.9608,0.9608,1),
        "seashell":(1,0.9608,0.9333,1),
        "beige":(0.9608,0.9608,0.8627,1),
        "oldlace":(0.9922,0.9608,0.902,1),
        "floralwhite":(1,0.9804,0.9412,1),
        "ivory":(1,1,0.9412,1),
        "antiquewhite":(0.9804,0.9216,0.8431,1),
        "linen":(0.9804,0.9412,0.902,1),
        "lavenderblush":(1,0.9412,0.9608,1),
        "mistyrose":(1,0.8941,0.8824,1),
        "gainsboro":(0.8627,0.8627,0.8627,1),
        "lightgray":(0.8275,0.8275,0.8275,1),
        "lightgrey":(0.8275,0.8275,0.8275,1),
        "silver":(0.7529,0.7529,0.7529,1),
        "darkgray":(0.6627,0.6627,0.6627,1),
        "darkgrey":(0.6627,0.6627,0.6627,1),
        "gray":(0.502,0.502,0.502,1),
        "grey":(0.502,0.502,0.502,1),
        "dimgray":(0.4118,0.4118,0.4118,1),
        "dimgrey":(0.4118,0.4118,0.4118,1),
        "lightslategray":(0.4667,0.5333,0.6,1),
        "lightslategrey":(0.4667,0.5333,0.6,1),
        "slategray":(0.4392,0.502,0.5647,1),
        "slategrey":(0.4392,0.502,0.5647,1),
        "darkslategray":(0.1843,0.3098,0.3098,1),
        "darkslategrey":(0.1843,0.3098,0.3098,1),
        "black":(0,0,0,1)
    }
    return colours

