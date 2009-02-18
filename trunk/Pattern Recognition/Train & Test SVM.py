#!coding: utf-8
from svm import *
import os, sys
import Image

import psyco
psyco.full()



TRAINING_FOLDER = 'DBTraining'
TEST_FOLDER = 'DBTest'
VERBOSE = 0
#MODEL_FILE = ""
MODEL_FILE = "model.svm"
GENERATE_ANYWAY = 1

if not os.path.isfile(MODEL_FILE) or GENERATE_ANYWAY:
    #Si le modèle n'existe pas ou que l'on veut spécifie GENERATE_ANYWAY=True, on le génère. Sinon, on le charge.
    
    print """
    ##############################################################################
    ############################    TRAINING    ##################################
    ##############################################################################
    """

    labels = []
    samples = []

    print "LOADING IMAGES..."

    train_elem = '3de2mt'

    for folder, subfolders, files in os.walk(TRAINING_FOLDER):
        if folder[-1] in train_elem:
            for file in [file for file in files if 'bmp' in file]:
                #print file
                im = Image.open(os.path.join(folder, file))
                labels.append(ord(folder[-1])-65)
                samples.append(map(lambda e:e/255., list(im.getdata())))
    print "Done.\n"

    print "GENERATING MODEL..."

    problem = svm_problem(labels, samples);
    size = len(samples)

    #param = svm_parameter(C = 10,nr_weight = 2,weight_label = [1,0],weight = [10,1], probability=1)
    param = svm_parameter(kernel_type = RBF, C=100, probability = 1,gamma=1.15)

    #kernels : LINEAR, POLY, RBF, and SIGMOID
    #types : C_SVC, NU_SVC, ONE_CLASS, EPSILON_SVR, and NU_SVR

    model = svm_model(problem,param)
    model.save(MODEL_FILE)
    
    print "Done.\n"

else:
    model = svm_model(MODEL_FILE)
    print "Model successfully loaded."
    

def predict(model, chemin_image):
    
    if not os.path.isfile(chemin_image):
        print "FICHIER INEXISTANT"
        return
    
    data = list(Image.open(chemin_image).convert('L').getdata())
    data = map(lambda e:e/255., data)
    
    prediction = model.predict(data)
    probability = model.predict_probability(data)  
    
    if VERBOSE:
        print probability
    
    return prediction


def analyze_folder(folder):
    errors = 0
    nb = 0
    for folder, subfolders, files in os.walk(folder):
        for file in [file for file in files if 'bmp' in file]:
            prediction = predict(model, os.path.join(folder, file))
            if prediction != ord(folder[-1])-65:
                errors += 1
            nb += 1
    print "Errors: %d / %d\n" % (errors, nb)



print """
##############################################################################
############################    TEST MODEL    ################################
##############################################################################
"""

print "Test on training set:"
print "---------------------"
for subdir in os.listdir(TRAINING_FOLDER):
    print "Testing on", subdir[-1]
    analyze_folder(os.path.join(TRAINING_FOLDER, subdir))


print "Test on test set:"
print "-----------------"
for subdir in os.listdir(TEST_FOLDER):
    print "Testing on", subdir[-1]
    analyze_folder(os.path.join(TEST_FOLDER, subdir))


raw_input()

