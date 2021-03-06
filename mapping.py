# -*- coding: utf-8 -*-


# replace <tr>\s*<td[^>]*>\s*<p> with [
# replace </p>\s*</td>\s*<td[^>]*>\s*<p> with ,
# replace </p>\s*</td>\s*</tr> with ]

import iso3166

# this will contain final mappings, all rows in this format:
# [range start, range end, country 2 letter code] for example:
# ['001','002', 'ir']
mappings = []
_mappings = [
    [0, 19, 'United States'],
    [20, 29, 'Restricted distribution (MO defined)'],
    [30, 39, 'United States'],
    [40, 49, 'Restricted distribution (MO defined)'],
    [50, 59, 'Coupons'],
    [60, 139, 'United States'],
    [200, 299, 'Restricted distribution (MO defined)'],
    [300, 379, 'France'],
    [380, 'Bulgaria'],
    [383, 'Slovenia'],
    [385, 'Croatia'],
    [387, 'Bosnia and Herzegovina'],
    [389, 'Montenegro'],
    [400, 440, 'Germany'],
    [450, 459, 'Japan'],
    [490, 499, 'Japan'],
    [460, 469, 'Russia'],
    [470, 'Kyrgyzstan'],
    [471, 'Taiwan'],
    [474, 'Estonia'],
    [475, 'Latvia'],
    [476, 'Azerbaijan'],
    [477, 'Lithuania'],
    [478, 'Uzbekistan'],
    [479, 'Sri Lanka'],
    [480, 'Philippines'],
    [481, 'Belarus'],
    [482, 'Ukraine'],
    [484, 'Moldova'],
    [485, 'Armenia'],
    [486, 'Georgia'],
    [487, 'Kazakhstan'],
    [488, 'Tajikistan'],
    [489, 'Hong Kong'],
    [500, 509, 'UK'],
    [520, 521, 'Greece'],
    [528, 'Lebanon'],
    [529, 'Cyprus'],
    [530, 'Albania'],
    [531, 'Macedonia'],
    [535, 'Malta'],
    [539, 'Ireland'],
    [540, 549, 'Belgium'],
    [560, 'Portugal'],
    [569, 'Iceland'],
    [570, 579, 'Denmark'],
    [590, 'Poland'],
    [594, 'Romania'],
    [599, 'Hungary'],
    [600, 601, 'South Africa'],
    [603, 'Ghana'],
    [604, 'Senegal'],
    [608, 'Bahrain'],
    [609, 'Mauritius'],
    [611, 'Morocco'],
    [613, 'Algeria'],
    [615, 'Nigeria'],
    [616, 'Kenya'],
    [618, u'Côte d\'Ivoire'],
    [619, 'Tunisia'],
    [620, 'Tanzania'],
    [621, 'Syria'],
    [622, 'Egypt'],
    [623, 'Brunei'],
    [624, 'Libya'],
    [625, 'Jordan'],
    [626, 'Iran'],
    [627, 'Kuwait'],
    [628, 'Saudi Arabia'],
    [629, 'Emirates'],
    [640, 649, 'Finland'],
    [690, 699, 'China'],
    [700, 709, 'Norway'],
    [729, 'Israel'],
    [730, 739, 'Sweden'],
    [740, 'Guatemala'],
    [741, 'El Salvador'],
    [742, 'Honduras'],
    [743, 'Nicaragua'],
    [744, 'Costa Rica'],
    [745, 'Panama'],
    [746, 'Dominican Republic'],
    [750, 'Mexico'],
    [754, 755, 'Canada'],
    [759, 'Venezuela'],
    [760, 769, 'Switzerland'],
    [770, 771, 'Colombia'],
    [773, 'Uruguay'],
    [775, 'Peru'],
    [777, 'Bolivia'],
    [778, 779, 'Argentina'],
    [780, 'Chile'],
    [784, 'Paraguay'],
    [786, 'Ecuador'],
    [789, 790, 'Brazil'],
    [800, 839, 'Italy'],
    [840, 849, 'Spain'],
    [850, 'Cuba'],
    [858, 'Slovakia'],
    [859, 'Czech'],
    [860, 'Serbia'],
    [865, 'Mongolia'],
    [867, 'Korea, Democratic People\'s Republic of'],
    [868, 869, 'Turkey'],
    [870, 879, 'Netherlands'],
    [880, 'Korea, Republic of'],
    [884, 'Cambodia'],
    [885, 'Thailand'],
    [888, 'Singapore'],
    [890, 'India'],
    [893, 'Viet nam'],
    [896, 'Pakistan'],
    [899, 'Indonesia'],
    [900, 919, 'Austria'],
    [930, 939, 'Australia'],
    [940, 949, 'New Zealand'],
    [950, 'Global Office'],
    [951, 'Global Office (EPCglobal)'],
    [955, 'Malaysia'],
    [958, 'Macao'],
    [960, 969, 'Global Office (GTIN-8s)'],
    [977, 'Serial publications (ISSN)'],
    [978, 979, 'Bookland (ISBN)'],
    [980, 'Refund receipts'],
    [981, 984, 'coupon identification for common currency areas'],
    [990, 999, 'coupon identification']]


def find_country(name):
    for c in iso3166.countries:
        if c.name.upper().startswith(name.upper()):
            return c
    # check if any names contains that
    for c in iso3166.countries:
        if name.upper() in c.name.upper():
            return c
    raise KeyError


for c in _mappings:
    try:
        ccode = find_country(c[-1]).alpha2.lower()
        range_start = "%03d" % c[0]
        if len(c) > 2:
            range_end = "%03d" % c[1]
        else:
            range_end = range_start
        mappings.append([range_start, range_end, ccode, c[-1]])
    except KeyError:
        print "Could not lookup '%s' in countries" % c[-1]