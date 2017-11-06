import sys
import math

def chunks(l, n):
    '''
    Yield successive n-sized chunks from l.
    Last chunk can be smaller.
    '''
    for i in range(0, len(l), n):
        yield l[i:i + n]

flatten = lambda l: [item for sublist in l for item in sublist]

#All FINAL  (for Training)
# (bad subjects removed: 994273, 937160, 885975, 788876, 713239)
# (no CA: 885975, 788876, 713239)
all_subjects_FINAL = ["992774", "991267", "987983", "984472", "983773", "979984", "978578", "965771", "965367", "959574",
                    "958976", "957974", "951457", "932554", "930449", "922854", "917255", "912447", "910241", "907656",
                    "904044", "901442", "901139", "901038", "899885", "898176", "896879", "896778", "894673", "889579",
                    "887373", "877269", "877168", "872764", "872158", "871964", "871762", "865363", "861456", "859671",
                    "857263", "856766", "849971", "845458", "837964", "837560", "833249", "833148", "826454", "826353",
                    "816653", "814649", "802844", "792766", "792564", "789373", "786569", "784565", "782561", "779370",
                    "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348", "749361", "748662",
                    "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "709551", "705341",
                    "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968",
                    "673455", "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236",
                    "620434", "613538", "601127", "599671", "599469"]   #105

#Tmp - probmap_xyz_to_mean.py
# all_subjects_FINAL = ["901038", "899885", "898176", "896879", "896778", "894673", "889579",
#                     "887373", "877269", "877168", "872764", "872158", "871964", "871762", "865363", "861456", "859671",
#                     "857263", "856766", "849971", "845458", "837964", "837560", "833249", "833148", "826454", "826353",
#                     "816653", "814649", "802844", "792766", "792564", "789373", "786569", "784565", "782561", "779370",
#                     "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348", "749361", "748662",
#                     "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "709551", "705341",
#                     "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968",
#                     "673455", "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236",
#                     "620434", "613538", "601127", "599671", "599469"]   #105

# all_subjects_FINAL = ["983773", "979984", "978578", "965771", "965367", "959574",
#                     "958976", "957974", "951457", "932554", "930449", "922854", "917255", "912447", "910241", "907656",
#                     "904044", "901442", "901139", "901038", "899885", "898176", "896879", "896778", "894673", "889579",
#                     "887373", "877269", "877168", "872764", "872158", "871964", "871762", "865363", "861456", "859671",
#                     "857263", "856766", "849971", "845458", "837964", "837560", "833249", "833148", "826454", "826353",
#                     "816653", "814649", "802844", "792766", "792564", "789373", "786569", "784565", "782561", "779370",
#                     "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348", "749361", "748662",
#                     "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "709551", "705341",
#                     "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968",
#                     "673455", "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236",
#                     "620434", "613538", "601127", "599671", "599469"]   #105



def get_all_subjects():
    '''
    This can be imported in other parts of project to get subjects
    '''
    return all_subjects_FINAL

#
# Info
#
# Start subjects ob batches:
#   n=2: 994273, 802844
#   n=4: 994273, 896879, 792766, 705341
#

#First
# all_subjects_RAW = ["994273"]
#First 10
# all_subjects_RAW = ["994273", "992774", "991267", "987983", "984472", "983773", "979984", "978578", "965771", "965367"]
#First 30
# all_subjects_RAW = ["994273", "992774", "991267", "987983", "984472", "983773", "979984", "978578", "965771", "965367", "959574", "958976",
#                 "957974", "951457", "937160", "932554", "930449", "922854", "917255", "912447", "910241", "907656", "904044", "901442",
#                 "901139", "901038", "899885", "898176", "896879", "896778"]
#Bad Outliers subjects
# all_subjects_RAW = ["994273", "937160", "885975", "859671", "713239"]

#All With Outliers  (for Preprocessing)
all_subjects_RAW = ["994273", "992774", "991267", "987983", "984472", "983773", "979984", "978578", "965771", "965367", "959574", "958976",
                "957974", "951457", "937160", "932554", "930449", "922854", "917255", "912447", "910241", "907656", "904044", "901442",
                "901139", "901038", "899885", "898176", "896879", "896778", "894673", "889579", "887373", "885975", "877269", "877168",
                "872764", "872158", "871964", "871762", "865363", "861456", "859671", "857263", "856766", "849971", "845458", "837964",
                "837560", "833249", "833148", "826454", "826353", "816653", "814649", "802844", "792766", "792564", "789373", "788876",
                "786569", "784565", "782561", "779370", "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348",
                "749361", "748662", "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "713239", "709551",
                "705341", "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968", "673455",
                "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538", "601127",
                "599671", "599469"] #110



#Merge Recobundles lowRes Part 1
# all_subjects_RAW = ["994273", "992774", "991267", "987983", "984472", "983773", "979984", "978578", "965771", "965367", "959574", "958976",
#                 "957974", "951457", "937160", "932554", "930449", "922854", "917255", "912447", "910241", "907656", "904044", "901442",
#                 "901139", "901038", "899885", "898176", "896879", "896778", "894673", "889579", "887373", "885975", "877269", "877168",
#                 "872764", "872158", "871964", "871762", "865363", "861456", "859671", "857263", "856766", "849971", "845458", "837964",
#                 "837560", "833249", "833148", "826454", "826353", "816653", "814649", "802844", "792766", "792564", "789373", "788876",
#                 "786569", "784565", "782561", "779370", "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348",
#                 "749361", "748662", "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "713239", "709551",
#                 "705341", "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968", "673455",
#                 "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538"]

# #Merge Recobundles lowRes Part 2
# all_subjects_RAW = ["601127", "599671", "599469"]

#Merge Recobundles - Rest after Bug -
# all_subjects_RAW = ["910241", "907656", "904044", "901442",
#                 "901139", "901038", "899885", "898176", "896879"]
# all_subjects_RAW = ["912447"]

#Tmp - Tracula
# all_subjects_RAW = ["814649", "802844", "792766", "792564", "789373", "788876",
#                 "786569", "784565", "782561", "779370", "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348",
#                 "749361", "748662", "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "713239", "709551",
#                 "705341", "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968", "673455",
#                 "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538", "601127",
#                 "599671", "599469"]

#Tmp - Tracula 2 (step1)
# all_subjects_RAW = ["734045", "732243", "729557", "729254", "715647", "715041", "713239", "709551",
#                 "705341", "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968", "673455",
#                 "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538", "601127",
#                 "599671", "599469"]

#Tmp - Tracula 2 (step2)
# all_subjects_RAW = ["680957", "679568", "677968", "673455",
#                 "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538", "601127",
#                 "599671", "599469"]


#Tmp - Recobundles lowRes
# all_subjects_RAW = ["654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538", "601127",
#                 "599671", "599469"] #110

#Tmp - recobundles lowRes
# all_subjects_RAW = ["705341", "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968", "673455",
#                     "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538", "601127",
#                     "599671", "599469"]

#Tmp - WMA LowRes
# all_subjects_RAW = ["912447", "910241", "907656", "904044", "901442",
#                 "901139", "901038", "899885", "898176", "896879", "896778", "894673", "889579", "887373", "885975", "877269", "877168",
#                 "872764", "872158", "871964", "871762", "865363", "861456", "859671", "857263", "856766", "849971", "845458", "837964",
#                 "837560", "833249", "833148", "826454", "826353", "816653", "814649", "802844", "792766", "792564", "789373", "788876",
#                 "786569", "784565", "782561", "779370", "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348",
#                 "749361", "748662", "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "713239", "709551",
#                 "705341", "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968", "673455",
#                 "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236", "620434", "613538", "601127",
#                 "599671", "599469"] #110


#TRACED
# all_subjects_RAW = ["s2_9"]

def get_all_subjects_RAW():
    return all_subjects_RAW

def get_subjects_chunk(nr_batches, batch_number):
    nr_batches = int(nr_batches)
    batch_number = int(batch_number)

    batch_size = int(math.ceil(len(all_subjects_RAW) / float(nr_batches)))
    res = list(chunks(all_subjects_RAW, batch_size))
    final_subjects = res[batch_number]
    return final_subjects

def main():
    '''
    This can be used in Shell scripts to get subjects
    '''
    args = sys.argv[1:]
    nr_batches = int(args[0])  # Number of batches
    batch_number = int(args[1])  # Which batch do we want     (idx starts at 0)

    batch_size = int(math.ceil(len(all_subjects_RAW) / float(nr_batches)))
    res = list(chunks(all_subjects_RAW, batch_size))

    #Note: can not print anyhting, because goes as parameter to script
    # print("Nr of Batches: {} (last batch might be smaller)".format(len(res)))
    # print("Nr of subjects in batch: {}".format(batch_size))
    final_subjects = res[batch_number]
    # print("Subjects: {}".format(final_subjects))

    #To String:
    str = ""
    for subject in final_subjects:
        str += subject + " "
    str = str[:-1]  #remove last space
    print(str)

if __name__ == "__main__":
    main()