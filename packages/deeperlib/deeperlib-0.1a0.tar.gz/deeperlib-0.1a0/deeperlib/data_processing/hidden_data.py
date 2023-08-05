import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
import os
from data_process import wordset


class HiddenData:
    """
    A HiddenData object would keep the data crawled from api in json format in a dict. It provides you
    with some methods to manipulate the data, such as, defining your own way to pre-process the
    raw_data, saving the data and matched pairs to files.
    """

    def __init__(self, result_dir, uniqueid, matchlist):
        """
        Initialize the object. The data structures of messages returned by various api are so different
        that users or developers have to define the uniqueid and matchlist of the messages manually.

        :param result_dir: the target directory for output files.
        :param uniqueid: the uniqueid of returned messages.
        :param matchlist: the fields of returned messages for similarity join.
        """
        self.setResultDir(result_dir)
        self.setUniqueId(uniqueid)
        self.setMatchList(matchlist)
        self.setMergeResult({})

    def proResult(self, result_raw):
        """
        Merge the raw data and keep them in a dict. Then, pre-process the raw data for similarity join.

        :param result_raw: the raw result returned by api.
        :return: a list for similarity join. [(['yong', 'jun', 'he', 'simon', 'fraser'],'uniqueid')]
        :raises KeyError: some messages would miss some fields.
        """
        result_merge = self.__mergeResult
        result_er = []
        for row in result_raw:
            try:
                r_id = eval(self.__uniqueId)
            except KeyError:
                continue
            if r_id not in result_merge:
                result_merge[r_id] = row
                bag = []
                for v in self.__matchList:
                    try:
                        bag.extend(wordset(eval(v)))
                    except KeyError:
                        continue
                result_er.append((bag, r_id))
        self.setMergeResult(result_merge)
        return result_er

    def saveResult(self):
        """
        Save the returned massages in the target directory.
        """
        resultList = self.__mergeResult.values()
        if not os.path.exists(self.__resultDir):
            os.makedirs(self.__resultDir)
        with open(self.__resultDir + '\\result_file', 'wb') as f:
            pickle.dump(resultList, f)

    def saveMatchPair(self):
        """
        Save the matched pairs judged by similarity join in the target directory.
        """
        savePair = {}
        for m in self.__matchPair:
            savePair[m[0]] = []
        for m in self.__matchPair:
            savePair[m[0]].append(m[1])
        if not os.path.exists(self.__resultDir):
            os.makedirs(self.__resultDir)
        with open(self.__resultDir + '\\match_file', 'wb') as f:
            pickle.dump(savePair, f)

    def setResultDir(self, result_dir):
        self.__resultDir = result_dir

    def getResultDir(self):
        return self.__resultDir

    def setUniqueId(self, uniqueid):
        self.__uniqueId = uniqueid

    def getUniqueId(self):
        return self.__uniqueId

    def setMatchList(self, matchlist):
        self.__matchList = matchlist

    def getMatchList(self):
        return self.__matchList

    def setMatchPair(self, matchpair):
        self.__matchPair = matchpair

    def getMatchPair(self):
        return self.__matchPair

    def setMergeResult(self, mergeresult):
        self.__mergeResult = mergeresult

    def getMergeResult(self):
        return self.__mergeResult
