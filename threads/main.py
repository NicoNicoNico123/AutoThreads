from chain import interact_chain
from serapi import SerpAPI
from threads import Threads

class Main:
    result = SerpAPI().main()
    output = interact_chain(result)
    Threads().main(output)

if __name__ == "__main__":
    Main()
