# [SS-1]: Target Estimates #

+ Version = 0.0.4
+ Date_TCT = 31.03.2025@05.28.31
+ Date_EST = 3.31.2025@01.28.31.AM

## [SS-1.1]: Torn Link Schemas ##

    <!-- @Torn: This Will Load a Players Profile -->
    + torn.com/profiles.php?XID={ID}

    <!-- @Torn: This Will Load a Target into the Attack Loader -->
    + torn.com/loader.php?sid=attack&user2ID={ID}

## [SS-1.2]: TornAPI Link Schemas ##

    <!-- @TornAPI: This Will Fetch a Targets Personal Stats -->
    + api.torn.com/user/{ID}?selections=personalstats&key={KEY}&comment={COMMENT}
        - attackswon
        - attackslost
        - attacksdraw
        - attacksassisted
        - defendswon
        - defendslost
        - defendsstalemated
        - elo
        - yourunaway
        - theyrunaway
        - unarmoredwon
        - bestkillstreak
        - attackhits
        - attackmisses
        - attackdamage
        - bestdamage
        - onehitkills
        - attackcriticalhits
        - roundsfired
        - specialammoused
        - hollowammoused
        - tracerammoused
        - piercingammoused
        - incendiaryammoused
        - attacksstealthed
        - retals
        - moneymugged
        - largestmug
        - itemslooted
        - highestbeaten
        - respectforfaction
        - rankedwarhits
        - raidhits
        - territoryjoins
        - territoryclears
        - territorytime
        - jobpointsused
        - trainsrecieved
        - itemsbought
        - auctionswon
        - auctionsells
        - itemssent
        - trades
        - cityitemsbought
        - pointsbought
        - pointssold
        - bazaarcustomers
        - bazaarsales
        - bazaarprofit
        - jailed
        - peoplebusted
        - failedbusts
        - peoplebought
        - peopleboughtspent
        - hospital
        - medicalitemsused
        - bloodwithdrawn
        - reviveskill
        - revives
        - revivesreceived
        - heahits
        - machits
        - rifhits
        - smghits
        - shohits
        - pishits
        - grehits
        - piehits
        - slahits
        - axehits
        - chahits
        - h2hhits
        - mailssent
        - friendmailssent
        - factionmailssent
        - companymailssent
        - spousemailssent
        - classifiedadsplaced
        - personalsplaced
        - criminaloffenses
        - vandalism
        - theft
        - counterfeiting
        - fraud
        - illicitservices
        - cybercrime
        - extortion
        - illegalproduction
        - organisedcrimes
        - searchforcashskill
        - bootleggingskill
        - graffitiskill
        - shopliftingskill
        - pickpocketingskill
        - cardskimmingskill
        - burglaryskill
        - hustlingskill
        - disposalskill
        - crackingskill
        - forgeryskill
        - scammingskill
        - bountiesplaced
        - totalbountyspent
        - bountiescollected
        - totalbountyreward
        - bountiesreceived
        - receivedbountyvalue
        - cityfinds
        - dumpfinds
        - itemsdumped
        - booksread
        - boostersused
        - consumablesused
        - candyused
        - alcoholused
        - energydrinkused
        - statenhancersused
        - eastereggs
        - eastereggsused
        - virusescoded
        - traveltimes
        - traveltime
        - itemsboughtabroad
        - huntingskill
        - attackswonabroad
        - defendslostabroad
        - argtravel
        - mextravel
        - dubtravel
        - hawtravel
        - japtravel
        - lontravel
        - soutravel
        - switravel
        - chitravel
        - cantravel
        - caytravel
        - drugsused
        - overdosed
        - rehabs
        - rehabcost
        - cantaken
        - exttaken
        - kettaken
        - lsdtaken
        - opitaken
        - pcptaken
        - shrtaken
        - spetaken
        - victaken
        - xantaken
        - missionscompleted
        - contractscompleted
        - dukecontractscompleted
        - missioncreditsearned
        - racingskill
        - racingpointsearned
        - racesentered
        - raceswon
        - networth
        - useractivity
        - activestreak
        - bestactivestreak
        - awards
        - nerverefills
        - tokenrefills
        - meritsbought
        - daysbeendonator
        - rankedwarringwins
        - arrestsmade
        - weaponsbought
        - dumpsearches
        - refills

    <!-- @TornAPI: This Will Fetch a Targets  -->
    + api.torn.com/user/{ID}?selections=&key={KEY}&comment={COMMENT}
        -

## [SS-1.3]: Things to Consider ##

    <!-- @MD: Styles -->
    1. *[Var]* = Italic Text
    2. **[Var]** = Bold Text
    3. ***[Var]*** = Bold & Italic

    <!-- @Calendar: Days per Month -->
    1. January = 31
    2. Febuary = 28 (29 @LeapYears)
    3. March = 31
    4. April = 30
    5. May = 31
    6. June = 30
    7. July = 31
    8. August = 31
    9. September = 30
    10. October = 31
    11. November = 30
    12. December = 31
    13. Total = 365 (366 @LeapYears)

    <!-- @Calendar: LeapYears -->
    + Years = 4
    + Prev = 2000
    + Prev = 2004
    + Prev = 2008
    + Prev = 2012
    + Prev = 2016
    + Prev = 2020
    + Last = 2024
    + Next = 2028
    + After = 2032
    + Future = 2036
    + Fututre = 2040
    <!-- @Time: How Many Seconds -->
    + Minute = 60
    + Hour = 3600
    + Day = 86400
    + Week = 604800
    + BiWeek = 1209600
    + 28Days = 2419200
    + 29Days = 2505600
    + 30Days = 2592000
    + 31Days = 2678400
    + Year = 31536000
    + LYear = 31622400

    <!-- @Time: How Many Minutes -->
    + Hour = 60
    + Day = 1440
    + Week = 10080
    + BiWeek = 20160
    + 28Days = 40320
    + 29Days = 41760
    + 30Days = 43200
    + 31Days = 44640
    + Year = 525600
    + LYear = 527040

# [SS-2]: 200m + #

## [SS-2.1]: UnOrdered ##

    | **Player ID** | Username | Tag | Lvl | Age | Last |
    | --- | --- | --- | --- | --- |

    + 2609694
        - Name = -Napos-
        - Tag = Idolized Damage Dealer
        - Lvl = 66
        - Age = 1641 (4y.5m.28d)
        - Last = 
        - TimePlayed =
        - HighestBeaten = 
        - 

## [SS-2.2]: Ordered ##

    + 24570
        - Name = BadMojo
        - Tag = Champion Punchbag
        - Lvl = 70
        - Age = 7325 (20y.0m.20d)
        - Last = 795 (2y. )
        - TimePlayed = 1017158 (11d.18h.)
        - HighestBeaten = 79
        - 

# [SS-3]: 20m - 200m #

## [SS-3.1]: UnOrdered ##

## [SS-3.2]: Ordered ##

    <!-- R+[5.0] -->

    <!-- R+[4.9] -->
    + 318930

    <!-- R+[4.8] -->


    <!-- R+[4.7] -->
    + 1062071
    + 30564

    <!-- R+[4.6] -->

    <!-- R+[4.5] -->
    + 2012030

    <!-- R+[4.4] -->
    + 922281

    <!-- R+[4.3] -->
    + 1037986

    <!-- R+[4.2] -->
    + 2349214
    + 2140093
    + 2093407

    <!-- R+[4.1] -->

    <!-- R+[4.0] -->
    + 420111
    + 147113

    <!-- R+[3.9] -->
    + 692277
    + 2485294

    <!-- R+[3.8] -->
    + 313702
    + 608201
    + 2561665
    + 2741356
    + 480341
    + 2773226
    + 661900
    + 1561277
    + 2104927
    + 2165222
    + 92182
    + 1582454
    + 944949
    + 2240071
    + 1964355
