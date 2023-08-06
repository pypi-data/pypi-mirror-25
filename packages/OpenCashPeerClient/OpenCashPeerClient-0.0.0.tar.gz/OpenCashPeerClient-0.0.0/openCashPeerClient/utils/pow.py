from multiprocessing import Pool, cpu_count
import hashlib

def printsomething():
    print("running from pow")

def checkHash(argsList):
    key = argsList[0]
    pattern = argsList[1]
    cpusNum = argsList[2]
    coreId = argsList[3]
    counter = coreId
    while True:
        counter += cpusNum
        newHash = hashlib.sha256()
        newFeed = key + ':' + str(counter)
        newHash.update(newFeed.encode('utf-8'))
        result = newHash.hexdigest()
        if result.startswith(pattern):
            return str(counter)

class POWGenerator:
    def __init__(self, key, difficulty, requestedCores):
        self.key = key
        self.beginningPattern = '0' * difficulty
        coresNum = cpu_count()
        if requestedCores <= coresNum:
            self.coresToUse = requestedCores
        else:
            self.coresToUse = coresNum
    

    def getSolution(self):
        jobsArgsList = []
        for cou in range(0,self.coresToUse):
            jobsArgsList.append((self.key, self.beginningPattern, self.coresToUse, cou))

        with Pool(processes=self.coresToUse) as workPool:
            for gotmatch in workPool.imap_unordered(checkHash, jobsArgsList):
                if gotmatch:
                    return gotmatch


if __name__ == "__main__":
    import sys
    key = sys.argv[1]
    difficulty = sys.argv[2]
    cores = sys.argv[3]
    gen = POWGenerator(key, int(difficulty), int(cores))
    print("Solution: {}".format(gen.getSolution()))