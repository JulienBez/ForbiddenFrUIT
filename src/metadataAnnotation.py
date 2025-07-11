
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.metrics import confusion_matrix
from nltk import agreement

from .utils import *

def getLabels(csv,merge=False):
    "MWE, UMWE, NONE, 4th case is UMWE with no MWE recognized, should not be possible" 
    labels = {}
    mwe = "expression_reconnue"
    umwe = "défigement_identifié"
    if merge:
        mwe = "expression_reconnue_finale"
        umwe = "défigement_identifié_final"
    for i in range(len(csv)):
        if csv['id'][i] not in labels:
            labels[csv['id'][i]] = ""
        if csv[umwe][i] == "oui" and csv[mwe][i] == "oui":
            labels[csv['id'][i]] = "PMWE" #change name from FR to EN if needed
        elif csv[umwe][i] == "non" and csv[mwe][i] == "oui":
            labels[csv['id'][i]] = "MWE" #change name from FR to EN if needed
        elif csv[umwe][i] == "non" and csv[mwe][i] == "non":
            labels[csv['id'][i]] = "None" #change name from FR to EN if needed
        else:
            print(f"ERROR WITH ID {csv['id'][i]}")
    return labels


def getAnnotationRes(sample):
    "save all annotation in a simple format ID:LABEL for each annotator"
    annotation_res = {}
    for path in glob.glob(f"data/all/common/{sample}/*/*.csv"):
        if "merge/" not in path:# and "3A/" not in path:
            annotator = path.split("/")[4]
            if annotator not in annotation_res:
                annotation_res[annotator] = {}
            csv = openPandasCSV(path)
            labels = getLabels(csv)
            for iid,label in labels.items():
                if iid not in annotation_res[annotator]:
                    annotation_res[annotator][iid] = label
                else:
                    annotation_res[annotator][f"{iid}2"] = label #we have a tweet which has been annotated twice, unfortunatly
    writeJson("data/annotation_matrix.json",annotation_res)


def getMergeAnnotationRes(sample):
    "save all annotation in a simple format ID:LABEL for the merged results"
    annotation_res = {}
    for path in glob.glob(f"data/all/common/{sample}/merge/*.csv"):
        annotator = path.split("/")[4]
        if annotator not in annotation_res:
            annotation_res[annotator] = {}
        csv = openPandasCSV(path)
        labels = getLabels(csv,merge=True)
        for iid,label in labels.items():
            if iid not in annotation_res[annotator]:
                annotation_res[annotator][iid] = label
            else:
                annotation_res[annotator][f"{iid}2"] = label #we have a tweet which has been annotated twice, unfortunatly
    return annotation_res


def computeConfusionMatrix(df,annotator_a,annotator_b):
    ""
    a_labels = df.loc[annotator_a].values
    b_labels = df.loc[annotator_b].values
    labels = np.unique(np.concatenate((a_labels, b_labels)))  #get all unique labels
    cm = confusion_matrix(a_labels,b_labels,labels=labels)
    return cm,labels


def saveConfusionMatrix(com,cm,labels,annotator_a,annotator_b,max=300,merge=False):
    "iterate once to see the max value, then change it accordingly"
    sns.heatmap(cm, annot=True,fmt='d',cmap='Oranges',xticklabels=labels,yticklabels=labels,vmin=0,vmax=max)
    plt.xlabel(annotator_a)
    plt.ylabel(annotator_b)
    if merge:
        plt.savefig(f"output/{com}_merged_confusion_matrix.png")
    else:
        plt.savefig(f"output/{com}_confusion_matrix_{annotator_a}_{annotator_b}.png")
    plt.close()


def getConfusionMatrix(com):
    "get confusion matrices between each possible pairs of annotators"

    data = openJson("data/annotation_matrix.json")
    df = pd.DataFrame.from_dict(data, orient='index')

    annotators = list(data.keys())
    pairs = [list(i) for i in combinations(annotators,2)]

    for pair in pairs:
        cm,labels = computeConfusionMatrix(df,pair[0],pair[1])
        saveConfusionMatrix(com,cm,labels,pair[0],pair[1],max=120)

    #print("Confusion Matrix between annotator_1 and annotator_2:\n", cm_1_2)
    #print("Confusion Matrix between annotator_2 and annotator_3:\n", cm_2_3)
    #print("Confusion Matrix between annotator_1 and annotator_3:\n", cm_1_3)


def mergeConfusionMatrix(df,labels):
    "get a merged confusion matrix between each and every annotators"

    true_labels = []
    pred_labels = []
        
    for annotator in df.index:
        for label in df.columns:
            true_labels.append(df.loc[annotator, label])
            pred_labels.append(df.loc[annotator, label])  #append true for the first annotator
                
            for other_annotator in df.index:
                if other_annotator != annotator:
                    pred_labels[-1] = df.loc[other_annotator, label]
                    true_labels.append(df.loc[annotator, label])
                    pred_labels.append(pred_labels[-1])

    return confusion_matrix(true_labels, pred_labels, labels=labels)


def getMergedConfusionMatrix(com):
    ""
    data = openJson("data/annotation_matrix.json")
    df = pd.DataFrame.from_dict(data, orient='index')
    all_labels = np.unique(df.values.flatten())
    combined_cm = mergeConfusionMatrix(df,all_labels)
    saveConfusionMatrix(com,combined_cm,all_labels,' ', ' ',max=800,merge=True)


def getInterAnnotatorAgreement():
    ""
    data = openJson("data/annotation_matrix.json")
    data_inter = []
    for key,value in data.items():
        for k,v in value.items():
            data_inter.append([key,k,v])
    ratingtask = agreement.AnnotationTask(data=data_inter)
    results = {
    #"kappa "  : ratingtask.kappa()#,
    #"fleiss " : ratingtask.multi_kappa()#,
    "alpha "  : ratingtask.alpha()#,
    #"scotts " : ratingtask.pi()
    }
    print(json.dumps(results, indent = 2))


def graphEchantillons(sample):
    "fonction créée pour visualiser l'accord inter-annotateur lors de la phase de test"
    annotators = ["A1","A2","A3","merge"]
    defigee = []
    reconnue = []
    nope = []
    data = {**openJson("data/annotation_matrix.json"),**getMergeAnnotationRes(sample)}
    for anno in annotators:
        defi = 0
        reco = 0
        no = 0
        for k,v in data[anno].items():
            if v == "PMWE" or v == "EMM défigée":
                defi += 1
            if v == "MWE" or v == "EMM":
                reco += 1
            if v == "None" or v == "pas d'EMM":
                no += 1
        defigee.append(defi)
        reconnue.append(reco)
        nope.append(no)
    defigee = np.array(defigee)
    reconnue = np.array(reconnue)
    nope = np.array(nope)
    x_axis = np.arange(len(annotators))
    #plt.style.use('seaborn-paper')
    sns.set_theme()
    #plt.ylim(0, 100)
    plt.bar(annotators, defigee, label = 'EMM défigées',color='coral')
    plt.bar(annotators, reconnue, bottom=defigee, label = 'EMM',color='cornflowerblue')
    plt.bar(annotators, nope, bottom=defigee+reconnue, label = 'None',color='limegreen')
    annotators[-1] = "Consensus"
    plt.xticks(x_axis, annotators)
    plt.legend()#loc='upper left' #bbox_to_anchor=(0.5, 0.98)
    plt.savefig(f'output/annotation_{sample}.png')
    plt.close()


def countTotalAnnotations(sample):
    ""
    data = getMergeAnnotationRes(sample)
    figement = len([1 for k,v in data["merge"].items() if v=="MWE"])
    defigement = len([1 for k,v in data["merge"].items() if v=="PMWE"])
    nothing = len([1 for k,v in data["merge"].items() if v=="None"])
    print(f"MWE:{figement}\nUMWE:{defigement}\nNone:{nothing}")


def getMetadata():
    ""
    createFolders("output")
    for com in ["1","2","3A","3B"]:
        getAnnotationRes(com)
        graphEchantillons(com)
        countTotalAnnotations(com)
        getInterAnnotatorAgreement()
        getConfusionMatrix(com)
        getMergedConfusionMatrix(com)