"""Restaurant data store with JSON persistence.

RESTAURANTS is loaded from db.json on startup.
All admin changes are automatically saved back to db.json.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TypedDict

logger = logging.getLogger(__name__)

DB_PATH: Path = Path(__file__).parent / "db.json"


class Restaurant(TypedDict, total=True):
    name: str
    phone: str
    address: str
    delivery: bool
    telegram: str
    maps: str


# ---------------------------------------------------------------------------
# Default data — all 50 US states
# ---------------------------------------------------------------------------

_DEFAULT_DATA: dict[str, list[Restaurant]] = {
    "Alabama": [
        {"name": "The Bright Star", "phone": "+1 (205) 424-9444", "address": "304 19th St N, Bessemer, AL 35020", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=The+Bright+Star+Bessemer+AL"},
        {"name": "Dreamland BBQ", "phone": "+1 (205) 933-2133", "address": "896 Tallapoosa St, Birmingham, AL 35217", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Dreamland+BBQ+Birmingham+AL"},
    ],
    "Alaska": [
        {"name": "Simon & Seafort's", "phone": "+1 (907) 274-3502", "address": "420 L St, Anchorage, AK 99501", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Simon+Seaforts+Anchorage+AK"},
        {"name": "Moose's Tooth Pub", "phone": "+1 (907) 258-2537", "address": "3300 Old Seward Hwy, Anchorage, AK 99503", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Mooses+Tooth+Anchorage+AK"},
    ],
    "Arizona": [
        {"name": "Barrio Café", "phone": "+1 (602) 636-0240", "address": "2814 N 16th St, Phoenix, AZ 85006", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Barrio+Cafe+Phoenix+AZ"},
        {"name": "Pizzeria Bianco", "phone": "+1 (602) 258-8300", "address": "623 E Adams St, Phoenix, AZ 85004", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Pizzeria+Bianco+Phoenix+AZ"},
        {"name": "El Charro Café", "phone": "+1 (520) 622-1922", "address": "311 N Court Ave, Tucson, AZ 85701", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=El+Charro+Cafe+Tucson+AZ"},
    ],
    "Arkansas": [
        {"name": "Doe's Eat Place", "phone": "+1 (501) 376-1195", "address": "1023 W Markham St, Little Rock, AR 72201", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Does+Eat+Place+Little+Rock+AR"},
        {"name": "The Faded Rose", "phone": "+1 (501) 663-9734", "address": "1619 Rebsamen Park Rd, Little Rock, AR 72202", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Faded+Rose+Little+Rock+AR"},
    ],
    "California": [
        {"name": "In-N-Out Burger", "phone": "+1 (800) 786-1000", "address": "4100 W Century Blvd, Inglewood, CA 90304", "delivery": True, "telegram": "https://t.me/innout_unofficial", "maps": "https://maps.google.com/?q=In-N-Out+Burger+Inglewood+CA"},
        {"name": "Nobu Los Angeles", "phone": "+1 (310) 343-5500", "address": "903 N La Cienega Blvd, Los Angeles, CA 90069", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Nobu+Los+Angeles+CA"},
        {"name": "Tartine Bakery", "phone": "+1 (415) 487-2600", "address": "600 Guerrero St, San Francisco, CA 94110", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Tartine+Bakery+San+Francisco+CA"},
    ],
    "Colorado": [
        {"name": "Buckhorn Exchange", "phone": "+1 (303) 534-9505", "address": "1000 Osage St, Denver, CO 80204", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Buckhorn+Exchange+Denver+CO"},
        {"name": "Snooze AM Eatery", "phone": "+1 (303) 297-0700", "address": "2262 Larimer St, Denver, CO 80205", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Snooze+AM+Eatery+Denver+CO"},
    ],
    "Connecticut": [
        {"name": "Frank Pepe Pizzeria", "phone": "+1 (203) 865-5762", "address": "157 Wooster St, New Haven, CT 06511", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Frank+Pepe+Pizzeria+New+Haven+CT"},
        {"name": "The Griswold Inn", "phone": "+1 (860) 767-1776", "address": "36 Main St, Essex, CT 06426", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Griswold+Inn+Essex+CT"},
    ],
    "Delaware": [
        {"name": "Dogfish Head Brewings", "phone": "+1 (302) 644-8292", "address": "320 Rehoboth Ave, Rehoboth Beach, DE 19971", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Dogfish+Head+Rehoboth+Beach+DE"},
        {"name": "Piccolo Italia", "phone": "+1 (302) 654-3610", "address": "1412 N DuPont St, Wilmington, DE 19806", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Piccolo+Italia+Wilmington+DE"},
    ],
    "Florida": [
        {"name": "Joe's Stone Crab", "phone": "+1 (305) 673-0365", "address": "11 Washington Ave, Miami Beach, FL 33139", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Joes+Stone+Crab+Miami+Beach"},
        {"name": "The Versailles Restaurant", "phone": "+1 (305) 444-0240", "address": "3555 SW 8th St, Miami, FL 33135", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Versailles+Restaurant+Miami"},
        {"name": "Bern's Steak House", "phone": "+1 (813) 251-2421", "address": "1208 S Howard Ave, Tampa, FL 33606", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Berns+Steak+House+Tampa+FL"},
    ],
    "Georgia": [
        {"name": "The Varsity", "phone": "+1 (404) 881-1706", "address": "61 North Ave NW, Atlanta, GA 30308", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=The+Varsity+Atlanta+GA"},
        {"name": "Bacchanalia", "phone": "+1 (404) 365-0410", "address": "1198 Howell Mill Rd, Atlanta, GA 30318", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Bacchanalia+Atlanta+GA"},
    ],
    "Hawaii": [
        {"name": "Alan Wong's", "phone": "+1 (808) 949-2526", "address": "1857 S King St, Honolulu, HI 96826", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Alan+Wongs+Honolulu+HI"},
        {"name": "Leonard's Bakery", "phone": "+1 (808) 737-5591", "address": "933 Kapahulu Ave, Honolulu, HI 96816", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Leonards+Bakery+Honolulu+HI"},
    ],
    "Idaho": [
        {"name": "The Gamekeeper", "phone": "+1 (208) 343-4611", "address": "800 W Main St, Boise, ID 83702", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Gamekeeper+Boise+ID"},
        {"name": "Fork Restaurant", "phone": "+1 (208) 287-1700", "address": "199 N 8th St, Boise, ID 83702", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Fork+Restaurant+Boise+ID"},
    ],
    "Illinois": [
        {"name": "Alinea", "phone": "+1 (312) 867-0110", "address": "1723 N Halsted St, Chicago, IL 60614", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Alinea+Chicago+IL"},
        {"name": "Lou Malnati's Pizzeria", "phone": "+1 (312) 828-9800", "address": "439 N Wells St, Chicago, IL 60654", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Lou+Malnatis+Chicago+IL"},
        {"name": "Portillo's", "phone": "+1 (312) 587-8910", "address": "100 W Ontario St, Chicago, IL 60654", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Portillos+Chicago+IL"},
    ],
    "Indiana": [
        {"name": "St. Elmo Steak House", "phone": "+1 (317) 635-0636", "address": "127 S Illinois St, Indianapolis, IN 46225", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=St+Elmo+Steak+House+Indianapolis+IN"},
        {"name": "Yats", "phone": "+1 (317) 686-6380", "address": "5363 N College Ave, Indianapolis, IN 46220", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Yats+Indianapolis+IN"},
    ],
    "Iowa": [
        {"name": "Zombie Burger", "phone": "+1 (515) 244-9292", "address": "300 E Grand Ave, Des Moines, IA 50309", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Zombie+Burger+Des+Moines+IA"},
        {"name": "Centro", "phone": "+1 (515) 248-1780", "address": "1003 Locust St, Des Moines, IA 50309", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Centro+Des+Moines+IA"},
    ],
    "Kansas": [
        {"name": "Chicken Annie's", "phone": "+1 (620) 231-9460", "address": "1143 E 600th Ave, Pittsburg, KS 66762", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Chicken+Annies+Pittsburg+KS"},
        {"name": "Radius Brewing", "phone": "+1 (620) 231-8888", "address": "610 N Broadway St, Pittsburg, KS 66762", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Radius+Brewing+Pittsburg+KS"},
    ],
    "Kentucky": [
        {"name": "Proof on Main", "phone": "+1 (502) 217-6360", "address": "702 W Main St, Louisville, KY 40202", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Proof+on+Main+Louisville+KY"},
        {"name": "Momma's Mustard & Pickles", "phone": "+1 (502) 638-0303", "address": "2661 Frankfort Ave, Louisville, KY 40206", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Mommas+Mustard+Pickles+Louisville+KY"},
    ],
    "Louisiana": [
        {"name": "Dooky Chase's", "phone": "+1 (504) 821-0600", "address": "2301 Orleans Ave, New Orleans, LA 70119", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Dooky+Chases+New+Orleans+LA"},
        {"name": "Commander's Palace", "phone": "+1 (504) 899-8221", "address": "1403 Washington Ave, New Orleans, LA 70130", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Commanders+Palace+New+Orleans+LA"},
        {"name": "Café Du Monde", "phone": "+1 (504) 525-4544", "address": "800 Decatur St, New Orleans, LA 70116", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Cafe+Du+Monde+New+Orleans+LA"},
    ],
    "Maine": [
        {"name": "Eventide Oyster Co.", "phone": "+1 (207) 774-8538", "address": "86 Middle St, Portland, ME 04101", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Eventide+Oyster+Portland+ME"},
        {"name": "The Lobster Shack", "phone": "+1 (207) 799-1677", "address": "222 Two Lights Rd, Cape Elizabeth, ME 04107", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Lobster+Shack+Cape+Elizabeth+ME"},
    ],
    "Maryland": [
        {"name": "The Choptank", "phone": "+1 (410) 244-8866", "address": "2000 Boston St, Baltimore, MD 21231", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=The+Choptank+Baltimore+MD"},
        {"name": "Woodberry Kitchen", "phone": "+1 (410) 464-8000", "address": "2010 Clipper Park Rd, Baltimore, MD 21211", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Woodberry+Kitchen+Baltimore+MD"},
    ],
    "Massachusetts": [
        {"name": "Legal Sea Foods", "phone": "+1 (617) 742-5300", "address": "255 State St, Boston, MA 02109", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Legal+Sea+Foods+Boston+MA"},
        {"name": "Mike's Pastry", "phone": "+1 (617) 742-3050", "address": "300 Hanover St, Boston, MA 02113", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Mikes+Pastry+Boston+MA"},
        {"name": "Oleana", "phone": "+1 (617) 661-0505", "address": "134 Hampshire St, Cambridge, MA 02139", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Oleana+Cambridge+MA"},
    ],
    "Michigan": [
        {"name": "American Coney Island", "phone": "+1 (313) 961-7758", "address": "114 W Lafayette Blvd, Detroit, MI 48226", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=American+Coney+Island+Detroit+MI"},
        {"name": "Zingerman's Deli", "phone": "+1 (734) 663-3354", "address": "422 Detroit St, Ann Arbor, MI 48104", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Zingermans+Deli+Ann+Arbor+MI"},
    ],
    "Minnesota": [
        {"name": "Alma Restaurant", "phone": "+1 (612) 379-4909", "address": "528 University Ave SE, Minneapolis, MN 55414", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Alma+Restaurant+Minneapolis+MN"},
        {"name": "Matt's Bar", "phone": "+1 (612) 722-7072", "address": "3500 Cedar Ave S, Minneapolis, MN 55407", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Matts+Bar+Minneapolis+MN"},
    ],
    "Mississippi": [
        {"name": "Doe's Eat Place", "phone": "+1 (662) 334-3315", "address": "502 Nelson St, Greenville, MS 38701", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Does+Eat+Place+Greenville+MS"},
        {"name": "Vestige", "phone": "+1 (228) 207-1733", "address": "715 Washington Ave, Ocean Springs, MS 39564", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Vestige+Ocean+Springs+MS"},
    ],
    "Missouri": [
        {"name": "Pappy's Smokehouse", "phone": "+1 (314) 535-4340", "address": "3106 Olive St, St. Louis, MO 63103", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Pappys+Smokehouse+St+Louis+MO"},
        {"name": "Arthur Bryant's BBQ", "phone": "+1 (816) 231-1123", "address": "1727 Brooklyn Ave, Kansas City, MO 64127", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Arthur+Bryants+BBQ+Kansas+City+MO"},
    ],
    "Montana": [
        {"name": "The Bitter Root", "phone": "+1 (406) 829-2981", "address": "101 Marcus St, Missoula, MT 59801", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Bitter+Root+Missoula+MT"},
        {"name": "Montana Club", "phone": "+1 (406) 442-5980", "address": "1 E Lawrence St, Helena, MT 59601", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Montana+Club+Helena+MT"},
    ],
    "Nebraska": [
        {"name": "Runza", "phone": "+1 (402) 423-2394", "address": "1625 South St, Lincoln, NE 68502", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Runza+Lincoln+NE"},
        {"name": "Dinker's Bar", "phone": "+1 (402) 346-7922", "address": "1036 S 10th St, Omaha, NE 68108", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Dinkers+Bar+Omaha+NE"},
    ],
    "Nevada": [
        {"name": "Joël Robuchon", "phone": "+1 (702) 891-7925", "address": "3799 S Las Vegas Blvd, Las Vegas, NV 89109", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Joel+Robuchon+Las+Vegas"},
        {"name": "In-N-Out Burger Las Vegas", "phone": "+1 (800) 786-1000", "address": "4888 Dean Martin Dr, Las Vegas, NV 89103", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=In-N-Out+Burger+Las+Vegas+NV"},
    ],
    "New Hampshire": [
        {"name": "The Black Trumpet", "phone": "+1 (603) 431-0887", "address": "29 Ceres St, Portsmouth, NH 03801", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Black+Trumpet+Portsmouth+NH"},
        {"name": "Colby's Breakfast & Lunch", "phone": "+1 (603) 436-3033", "address": "105 Daniel St, Portsmouth, NH 03801", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Colbys+Breakfast+Portsmouth+NH"},
    ],
    "New Jersey": [
        {"name": "Knife & Fork Inn", "phone": "+1 (609) 344-1133", "address": "3600 Atlantic Ave, Atlantic City, NJ 08401", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Knife+Fork+Inn+Atlantic+City+NJ"},
        {"name": "White Manna Hamburgers", "phone": "+1 (201) 342-0914", "address": "358 River St, Hackensack, NJ 07601", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=White+Manna+Hackensack+NJ"},
    ],
    "New Mexico": [
        {"name": "The Shed", "phone": "+1 (505) 982-9030", "address": "113 1/2 E Palace Ave, Santa Fe, NM 87501", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=The+Shed+Santa+Fe+NM"},
        {"name": "Duran's New Mexico Kitchen", "phone": "+1 (505) 247-4141", "address": "1800 Central Ave SW, Albuquerque, NM 87104", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Durans+New+Mexico+Kitchen+Albuquerque"},
    ],
    "New York": [
        {"name": "Katz's Delicatessen", "phone": "+1 (212) 254-2246", "address": "205 E Houston St, New York, NY 10002", "delivery": True, "telegram": "https://t.me/katzsny", "maps": "https://maps.google.com/?q=Katzs+Delicatessen+New+York"},
        {"name": "Le Bernardin", "phone": "+1 (212) 554-1515", "address": "155 W 51st St, New York, NY 10019", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Le+Bernardin+New+York"},
        {"name": "Joe's Pizza", "phone": "+1 (212) 366-1182", "address": "7 Carmine St, New York, NY 10014", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Joes+Pizza+New+York"},
    ],
    "North Carolina": [
        {"name": "Lexington Barbecue", "phone": "+1 (336) 249-9814", "address": "100 Smokehouse Ln, Lexington, NC 27295", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Lexington+Barbecue+NC"},
        {"name": "The Angus Barn", "phone": "+1 (919) 781-2444", "address": "9401 Glenwood Ave, Raleigh, NC 27617", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Angus+Barn+Raleigh+NC"},
    ],
    "North Dakota": [
        {"name": "Kroll's Diner", "phone": "+1 (701) 223-1440", "address": "1915 N 12th St, Bismarck, ND 58501", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Krolls+Diner+Bismarck+ND"},
        {"name": "Paradiso Mexican Restaurant", "phone": "+1 (701) 255-5555", "address": "1410 E Century Ave, Bismarck, ND 58503", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Paradiso+Mexican+Bismarck+ND"},
    ],
    "Ohio": [
        {"name": "Skyline Chili", "phone": "+1 (513) 241-2020", "address": "643 Vine St, Cincinnati, OH 45202", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Skyline+Chili+Cincinnati+OH"},
        {"name": "Michael Symon's Lola", "phone": "+1 (216) 621-5652", "address": "2058 E 4th St, Cleveland, OH 44115", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Lola+Bistro+Cleveland+OH"},
    ],
    "Oklahoma": [
        {"name": "Cattlemen's Steakhouse", "phone": "+1 (405) 236-0416", "address": "1309 S Agnew Ave, Oklahoma City, OK 73108", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Cattlemens+Steakhouse+Oklahoma+City"},
        {"name": "Nic's Grill", "phone": "+1 (405) 524-0999", "address": "1201 N Penn Ave, Oklahoma City, OK 73107", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Nics+Grill+Oklahoma+City"},
    ],
    "Oregon": [
        {"name": "Le Pigeon", "phone": "+1 (503) 546-8796", "address": "738 E Burnside St, Portland, OR 97214", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Le+Pigeon+Portland+OR"},
        {"name": "Voodoo Doughnut", "phone": "+1 (503) 241-4704", "address": "22 SW 3rd Ave, Portland, OR 97204", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Voodoo+Doughnut+Portland+OR"},
        {"name": "Jake's Famous Crawfish", "phone": "+1 (503) 226-1419", "address": "401 SW 12th Ave, Portland, OR 97205", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Jakes+Famous+Crawfish+Portland+OR"},
    ],
    "Pennsylvania": [
        {"name": "Reading Terminal Market", "phone": "+1 (215) 922-2317", "address": "51 N 12th St, Philadelphia, PA 19107", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Reading+Terminal+Market+Philadelphia+PA"},
        {"name": "Primanti Brothers", "phone": "+1 (412) 263-2142", "address": "46 18th St, Pittsburgh, PA 15222", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Primanti+Brothers+Pittsburgh+PA"},
    ],
    "Rhode Island": [
        {"name": "Al Forno", "phone": "+1 (401) 273-9760", "address": "577 S Main St, Providence, RI 02903", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Al+Forno+Providence+RI"},
        {"name": "Haven Brothers Diner", "phone": "+1 (401) 861-7777", "address": "Fulton St, Providence, RI 02903", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Haven+Brothers+Diner+Providence+RI"},
    ],
    "South Carolina": [
        {"name": "Husk Charleston", "phone": "+1 (843) 577-2500", "address": "76 Queen St, Charleston, SC 29401", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Husk+Charleston+SC"},
        {"name": "FIG Restaurant", "phone": "+1 (843) 805-5900", "address": "232 Meeting St, Charleston, SC 29401", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=FIG+Restaurant+Charleston+SC"},
    ],
    "South Dakota": [
        {"name": "Minerva's", "phone": "+1 (605) 334-0386", "address": "301 S Phillips Ave, Sioux Falls, SD 57104", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Minervas+Sioux+Falls+SD"},
        {"name": "Watiki Indoor Waterpark", "phone": "+1 (605) 718-4939", "address": "1314 N Elk Vale Rd, Rapid City, SD 57703", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Rapid+City+SD+restaurants"},
    ],
    "Tennessee": [
        {"name": "Prince's Hot Chicken", "phone": "+1 (615) 226-9442", "address": "123 Ewing Dr, Nashville, TN 37207", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Princes+Hot+Chicken+Nashville+TN"},
        {"name": "Rendezvous BBQ", "phone": "+1 (901) 523-2746", "address": "52 S 2nd St, Memphis, TN 38103", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Rendezvous+BBQ+Memphis+TN"},
        {"name": "The Loveless Cafe", "phone": "+1 (615) 646-9700", "address": "8400 TN-100, Nashville, TN 37221", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Loveless+Cafe+Nashville+TN"},
    ],
    "Texas": [
        {"name": "Franklin Barbecue", "phone": "+1 (512) 653-1187", "address": "900 E 11th St, Austin, TX 78702", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Franklin+Barbecue+Austin+TX"},
        {"name": "Uchi Austin", "phone": "+1 (512) 916-4808", "address": "801 S Lamar Blvd, Austin, TX 78704", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Uchi+Austin+TX"},
        {"name": "The Original Ninfa's", "phone": "+1 (713) 228-1175", "address": "2704 Navigation Blvd, Houston, TX 77003", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Ninfas+Houston+TX"},
    ],
    "Utah": [
        {"name": "Red Iguana", "phone": "+1 (801) 322-1489", "address": "736 W North Temple, Salt Lake City, UT 84116", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Red+Iguana+Salt+Lake+City+UT"},
        {"name": "The Roof Restaurant", "phone": "+1 (801) 539-1911", "address": "15 E Temple, Salt Lake City, UT 84150", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=The+Roof+Restaurant+Salt+Lake+City+UT"},
    ],
    "Vermont": [
        {"name": "Hen of the Wood", "phone": "+1 (802) 583-4503", "address": "55 Cherry St, Burlington, VT 05401", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Hen+of+the+Wood+Burlington+VT"},
        {"name": "Al's French Frys", "phone": "+1 (802) 862-9203", "address": "1251 Williston Rd, South Burlington, VT 05403", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Als+French+Frys+Burlington+VT"},
    ],
    "Virginia": [
        {"name": "The Inn at Little Washington", "phone": "+1 (540) 675-3800", "address": "309 Middle St, Washington, VA 22747", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Inn+at+Little+Washington+VA"},
        {"name": "Mama J's Kitchen", "phone": "+1 (804) 225-7449", "address": "415 N 1st St, Richmond, VA 23219", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Mama+Js+Kitchen+Richmond+VA"},
    ],
    "Washington": [
        {"name": "The Canlis", "phone": "+1 (206) 283-3313", "address": "2576 Aurora Ave N, Seattle, WA 98109", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Canlis+Seattle+WA"},
        {"name": "Pike Place Chowder", "phone": "+1 (206) 267-2537", "address": "1530 Post Alley, Seattle, WA 98101", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Pike+Place+Chowder+Seattle+WA"},
        {"name": "Ivar's Acres of Clams", "phone": "+1 (206) 624-6852", "address": "1001 Alaskan Way, Seattle, WA 98104", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Ivars+Acres+of+Clams+Seattle+WA"},
    ],
    "West Virginia": [
        {"name": "Pies & Pints", "phone": "+1 (304) 342-7437", "address": "222 Capitol St, Charleston, WV 25301", "delivery": True, "telegram": "", "maps": "https://maps.google.com/?q=Pies+Pints+Charleston+WV"},
        {"name": "The Greenbrier", "phone": "+1 (304) 536-1110", "address": "101 Main St W, White Sulphur Springs, WV 24986", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=The+Greenbrier+WV"},
    ],
    "Wisconsin": [
        {"name": "Supper Club", "phone": "+1 (414) 933-1000", "address": "2909 S Kinnickinnic Ave, Milwaukee, WI 53207", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Supper+Club+Milwaukee+WI"},
        {"name": "Old Fashioned Tavern", "phone": "+1 (608) 310-4545", "address": "23 W Mifflin St, Madison, WI 53703", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Old+Fashioned+Tavern+Madison+WI"},
    ],
    "Wyoming": [
        {"name": "Snake River Grill", "phone": "+1 (307) 733-0557", "address": "84 E Broadway Ave, Jackson, WY 83001", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Snake+River+Grill+Jackson+WY"},
        {"name": "The Blue Lion", "phone": "+1 (307) 733-3912", "address": "160 N Millward St, Jackson, WY 83001", "delivery": False, "telegram": "", "maps": "https://maps.google.com/?q=Blue+Lion+Jackson+WY"},
    ],
}


# ---------------------------------------------------------------------------
# JSON persistence
# ---------------------------------------------------------------------------

def _load() -> dict[str, list[Restaurant]]:
    """Load data from db.json, falling back to defaults if missing."""
    if DB_PATH.exists():
        try:
            with DB_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info("Loaded %d states from %s", len(data), DB_PATH)
                return data
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load db.json (%s), using defaults.", exc)
    logger.info("db.json not found — using built-in defaults.")
    return {k: list(v) for k, v in _DEFAULT_DATA.items()}


def save() -> None:
    """Persist current RESTAURANTS to db.json."""
    try:
        with DB_PATH.open("w", encoding="utf-8") as f:
            json.dump(RESTAURANTS, f, ensure_ascii=False, indent=2)
        logger.debug("Saved %d states to %s", len(RESTAURANTS), DB_PATH)
    except OSError as exc:
        logger.error("Failed to save db.json: %s", exc)


# Single mutable source of truth
RESTAURANTS: dict[str, list[Restaurant]] = _load()