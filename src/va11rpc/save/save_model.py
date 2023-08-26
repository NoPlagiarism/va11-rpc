class Save:
    ALL_VAR_NAMES = (
        "dt_string", 'ngplus_flag', 'cur_day', 'cur_client', 'cur_stage', 'barscore', 'jillwallet', 'datestring',
        'dayphase',
        'ft_any',
        'ft_alma', 'ft_stella', 'don1', 'don2', 'don3', 'dondrunk1', 'ing1', 'ing2', 'ing3', 'ingdrunk1', 'sei1',
        'sei2',
        'sei3', 'seidrunk1', 'kim1', 'kim2', 'kim3', 'kimdrunk1', 'don4', 'don5', 'don6', 'dondrunk2', 'dorodrink1',
        'dorodrink2', 'dorodrink3', 'dorodrunk1', 'jamie1', 'miki1', 'miki2', 'miki3', 'drunkmiki1', 'alma1', 'alma2',
        'alma3', 'almadrunk1', 'don7', 'don8', 'dondrunk2', 'stel1', 'stel2', 'stel3', 'steldrunk1', 'sei4', 'art1',
        'art2',
        'stream1', 'stream2', 'streamdrunk1', 'db1', 'db2', 'db3', 'bettydrunk1', 'jamie2', 'jamie3', 'dana1', 'tay1',
        'tay2', 'alma4', 'alma5', 'alma6', 'almadrunk2', 'dorodrink4', 'virgilio1', 'virgilio2', 'jilldrunk1', 'brian1',
        'brian2', 'stel4', 'stel5', 'art3', 'art4', 'art5', 'virgilio3', 'rad1', 'rad2', 'sei5', 'sei6', 'jamie4',
        'jamie5',
        'jamie6', 'ing4', 'ing5', 'ingdrunk2', 'norma1', 'mario1', 'mario2', 'mario3', 'dorodrink4', 'dorodrink5',
        'dorodrink6', 'dorodrunk2', 'virgilio4', 'virgilio5', 'virgilio6', 'sei7', 'stel6', 'stel7', 'stel8', 'kim4',
        'kim5', 'nacho3', 'db4', 'db5', 'alma7', 'alma8', 'jill1', 'jill2', 'dorodrink7', 'dorodrink8', 'dorodrink9',
        'sei8', 'sei9', 'truevirgilio1', 'truevirgilio2', 'truevirgilio3', 'art6', 'art7', 'lexi1', 'lexi2', 'stel9',
        'stel10', 'stel11', 'sei10', 'sei11', 'dorothy10', 'dorothy11', 'mario4', 'mario5', 'ing6', 'ing7', 'ing8',
        'alma9',
        'alma10', 'alma11', 'miki4', 'miki5', 'db6', 'db7', 'db8', 'stream3', 'stream4', 'dorothy12', 'dorothy13',
        'dorothy14', 'stream5', 'stream6', 'gabyorder', 'absinthe_add', 'rum_add', 'shop_tea', 'song1', 'song2',
        'song3',
        'song4', 'song5', 'song6', 'song7', 'song8', 'song9', 'song10', 'song11', 'song12', 'shop_casitas',
        'shop_maneki',
        'shop_miki', 'shop_poster', 'shop_poster', 'shop_carts', 'shop_daruma', 'shop_y2k', 'shop_snatcher',
        'shop_christmas', 'shop_turing', 'shop_crt', 'shop_fan', 'shop_plant', 'shop_shoulder', 'shop_beerlot',
        'shop_banner', 'shop_lamp', 'tealwall', 'creamwall', 'redwall', 'purplewall', 'blackwall', 'graywall',
        'whitewall',
        'greenwall', 'yellowwall', 'pinkwall', 'stripewall', 'cheetahwall', 'cirawall', 'cheetahtable', 'torpedotable',
        'stripetable', 'defaulttable', 'wallstype', 'kotatsutype', 'porndl', 'lightdl', 'housedl', 'hopesshop',
        'eltonsshop', 'havenshop', 'shootersong', 'barshop', 'endingshop', 'friendlyshop', 'gotmeshop', 'song1name',
        'song2name', 'song3name', 'song4name', 'song5name', 'song6name', 'song7name', 'song8name', 'song9name',
        'song10name', 'song11name', 'song12name', 'mistakecounter', 'flawless_chain', 'shooterdone', 'framebar',
        'wallpaperbar', 'streamingsong', 'mikisong', 'frontiersong', 'staffsong', 'ironheartsong', 'cashcounter',
        'tipcounter', 'mikiwall', 'juleswall', 'radwall')

    def __init__(self, values=None):
        if values:
            self.var_values = values
        else:
            self.var_values = [None] * len(self.ALL_VAR_NAMES)

    def __getitem__(self, item):
        if isinstance(item, str) and item in self.ALL_VAR_NAMES:
            return self.var_values[self.ALL_VAR_NAMES.index(item)]
        elif isinstance(item, int) and item >= 0:
            return self.var_values[item]
        raise KeyError()

    def __setitem__(self, key, value):
        old_value = self[key]
        self.var_values[self.var_values.index(old_value)] = value

    def __repr__(self):
        return f"{self['cur_day']} day. {self['barscore']}$. {self['dt_string']}{' NG+' if self['ngplus_flag'] else ''}"

    def get_as_dict(self):
        return dict(zip(self.ALL_VAR_NAMES, self.var_values))


def get_from_raw_lines(lines, cls=Save):
    # if "" == lines[-1]:
    #     lines = lines[:-1]
    for i in range(len(lines)):
        try:
            lines[i] = int(lines[i])
        except ValueError:
            lines[i] = lines[i].strip(" ")
    return cls(lines)


def read_save(path, cls=Save):
    with open(path, mode="r", encoding="utf-8") as f:
        raw = f.read().split("\n")
    return get_from_raw_lines(raw, cls=cls)
