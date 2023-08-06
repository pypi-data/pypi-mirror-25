from .utils import getRepos, getIssues, checkRate
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='Displays question likes for workshop talks')
    parser.add_argument('speaker', nargs='?', default=None, help='The speaker\'s name (or at least an unique substring) or number')
    parser.add_argument('-c', '--check-api', default = False, action='store_true', help = 'Check number of API calls remaining')
    parser.add_argument('-d', '--debug', default = False, action='store_true', help = 'debug mode')
    return parser.parse_args()

def askForSpeaker(repos):
    """Lock in a while loop and ask for the speaker as an integer"""
    try:
        while True:
            print("The avaiable speakers are:")
            for i, r in enumerate(repos):
                print("{}) {}".format(i + 1, r['name']))
            selection = input("Select the number of the speaker: ")
            try:
                s = int(selection) - 1
                targetRepo = repos[s]
            except:
                print("That is not a valid selection")
            else:
                return targetRepo
    except KeyboardInterrupt:
        print("\nExiting")
        return False

def main():
    """Get all the repos info, then figure which one the user wants. Finally print all the issues with their reactions"""
    args = parseArgs()
    repos = getRepos()

    remaining = checkRate()
    if args.check_api:
        print("There are {} API calls remaining".format(remaining))
    if args.debug:
        print(args)
    if remaining < 3:
        print("There are not enough API calls left on this IP address, wait 30-60 minutes then try again")
        return
    elif remaining < 10:
        print("Warning: There may not be enough API calls left on this IP address")
    if args.speaker is None:
        targetRepo = askForSpeaker(repos)
    else:
        try:
            #The displayed list is 1 indexed
            targetRepo = repos[int(args.speaker) - 1]
        except:
            selection = [r for r in repos if args.speaker in r['name']]
            if len(selection) == 0:
                print("{} was not found in any of the speaker's names")
                targetRepo = askForSpeaker(repos)
            elif len(selection) == 1:
                targetRepo = selection[0]
            else:
                print("{} was found in mutiple speaker's names".format(args.speaker))
                targetRepo = askForSpeaker(selection)
    if targetRepo:
        getIssues(targetRepo)

if __name__ == '__main__':
    main()
