# Code2vec model for clone detecting  
This is my technical work for JetBrains internship.

In this work I used code2vec model described in [1] and implemented in [2].

The main idea of the vector representation is that code snippets with the same meaning will mapped to simular vectors (respect Euclidean metric).

Then I specified threshold.
If distance between vectors will be smalle, I consider that they are clones.


## Requirements
On Ubuntu:
  * Python3 (3.5 < version < 3.8). To check the version:
> python3 --version
  * TensorFlow - version 2.0.0-beta1 ([install](https://www.tensorflow.org/install/install_linux)).
  To check TensorFlow version:
> python3 -c 'import tensorflow as tf; print(tf.\_\_version\_\_)'


## Quickstart

### Step 0: Install requirement packages
```
pip3 install --upgrade pip
pip3 install tensorflow==2.0.0-beta1
```

### Step 1: Cloning this repository
```
go to your working directory. Let's call it $root$
cd $root$
git clone https://github.com/Qvery-mm/JB-application
```

### Step 2: Downloading a trained model (1.4 GB)
Authors of tech-srl/code2vec already trained a model for 8 epochs on their own data.
This model can be downloaded [here](https://s3.amazonaws.com/code2vec/model/java14m_model.tar.gz) or using:
```
wget https://s3.amazonaws.com/code2vec/model/java14m_model.tar.gz
tar -xvzf java14m_model.tar.gz
```
Extract the contents into the JB-application directory

### Step 3: install BigCloneBench
------------------------------------------------------------------------------------------

```
cd $root$
git clone https://github.com/jeffsvajlenko/BigCloneEval
cd BigCloneEval
```

#### Download the latest version of IJaDataset (as specially packaged for BigCloneEval) from
the following webpage:

IJaDataset, BigCloneEval Version: https://www.dropbox.com/s/xdio16u396imz29/IJaDataset_BCEvalVersion.tar.gz?dl=0

Extract the contents of IJaDataset (IJaDataset_BCEvalVersion.tar.gz) into the 'ijadataset'
directory of the BigCloneEval distribution.

This should create a directory 'ijadataset/bcb_reduced/' which contains one sub-directory
per functionality in BigCloneBench.

#### Get the latest version of BigCloneBench database:

Downloaded the latest version of BigCloneBench (as specially packaged for BigCloneEval) 
from the following webpage:

https://www.dropbox.com/s/z2k8r78l63r68os/BigCloneBench_BCEvalVersion.tar.gz?dl=0

Extract the contents of BigCloneBench (BigCloneBench_BCEvalVersion.tar.gz) into the
'bigclonebenchdb' directory of the BigCloneEval distribution.

After that run ```make``` from the root directory of BigCloneEval

------------------------------------------------------------------------------------------
### Step 4: Initialize the tools 
------------------------------------------------------------------------------------------

Consider you are in the BigCloneEval directory

Go to the commands/ directory and execute the 'init' script.  This will initialize the tools
database.
```
cd commands
./init
```
Register tool

```
./registerTool -n "code2vec" -d "1 threshold"
```



### Step 5: Evaluating a trained model
Suppose that iteration #8 is our chosen model, run from JB-application directory:
```
python3 code2vec.py --load models/java14_model/saved_model_iter8.release --predict --export_code_vectors
```
Code2vec model quite large (1.4Gb) so script may not work on a small machines.

While evaluating, a number of files named "data<N>.csv" is written with each pair of clones in the following format:
```
<total number of snippets> <dimension of code vector>
```
Then 'rows' times following pattern will appear:
```
<dirname> <filename> <snippet line start> < snippet line end>
<384 dimensional vector>
```
Due to large size of dataset it may take a long time.
 
After complete you'll see 44 csv files in JB-application directory. (data2.csv - data45.csv)

Now you may compare cnippets by their vector representations:
```
cd cpp
g++ findClones.cpp -o findClones
./findClones
```

It may take a while.
If square distance between two vectors smaller than 60, then I decide that following snippets may be clones.

After that you'll see file named 'ClonesWithDistance'.
It contain a large number of following lines:
<dirname 1> <filename 1> <snippet line start 1> < snippet line end 1> <dirname 2> <filename 2> <snippet line start 2> < snippet line end 2> <square distance>

After that you must run the script named select.py
```
python3 select.py
```
And specify desired threshold (but not greater then 7.75)

I used =1

Now you'll see file named 'finalClones'

### Model estimation

### import clones
Go to the commands directory of BigCloneEval distribution and run: 
```
./importClones -t 1 -c ../../JB-application/cpp/finalClones
```
after importing run
```
./evaluateTool -t 1 -o code2vec.report
```
It will generate you report about your tool.

### Estimation of my model

My model found 72.547.615.152 pair of snippets and after computing distance there are 12724186 pairs of snippets, which distance less then 1 in their vector representation.
Let's denote 12724186 by numPairs
According report (see report/code2vec.report), model with fixed 1.0 
achieve following results:

     -- Recall Per Clone Type (type: numDetected / numClones = recall) --

     Type-1: 45540 / 47146 = 0.9659356042930471
             
     Type-2: 636 / 4609 = 0.13799088739422868
              
     Type-2 (blind): 174 / 386 = 0.45077720207253885
      
     Type-2 (consistent): 462 / 4223 = 0.10940089983424106
 
     Very-Strongly Type-3: 2246 / 4163 = 0.5395147730002402

     Strongly Type-3: 3049 / 16631 = 0.18333233118874392
     
     Moderatly Type-3: 316 / 83444 = 0.003786970902641292
    
     Weakly Type-3/Type-4: 120 / 8219320 = 1.4599747911019404E-5
     

Clone type sense

    Type-1 - strick match token by token after Type-1 normalisation
    Type-2 - strick match token by token after Type-2 normalisation
    Very-Strongly Type-3: Clone similarity in range [90,100) after pretty-printing and identifier/literal normalization.
    Strongly Type-3: Clone similarity in range [70, 90) after pretty-printing and identifier/literal normalization.
    Moderately Type-3: Clone similarity in range [50, 70) after pretty-printing and identifier/literal normalization.
    Weakly Type-3/Type-4: Clone similarity in range [ 0, 50) after pretty-printing and identifier/literal normalization.     

According definition of clone types, I decided do not track Moderately Type-3 and Weakly Type-3/Type-4 clones.
Thus I may estimate my model.

Recall = (sum 'numDetected' over all 'Types' except last 2) / (sum 'numClones' over all 'Types' except last 2)
```
Recall = 52107 / 77158 = 0.6753285466
```

Precision = numDetected / numPairs
```
Precision = 52107 / 12724186 = 0.0040951146
```

```
F1 = 0.00814086
```

Increasing of threreshould may improve recall for Type 3 and Type 4 clones but it will also lead to dramatically low precision. For example for threshold = 7.75 exists more 60.000.000.000 pairs of potential clones. In this case precision will be smaller than  10^-5.

# What's next?

It is clear, that current version of model has bad precision. There are some reasons for this.

At first, I used fixed threshold. Estimation may be better if threshold will depend on size of snippet. Such improvement described in some related papers.

Secondly, I should select small subset of dataset and use optimisation algorithm on it in order to find the best threshold.

Finally, it is possible to use more complex model in opposite simple pairwise comparing.


# Citation

[1] [code2vec: Learning Distributed Representations of Code](https://urialon.cswp.cs.technion.ac.il/wp-content/uploads/sites/83/2018/12/code2vec-popl19.pdf) github.com/tech-srl/code2vec

[2] [Uri Alon](http://urialon.cswp.cs.technion.ac.il), [Meital Zilberstein](http://www.cs.technion.ac.il/~mbs/), [Omer Levy](https://levyomer.wordpress.com) and [Eran Yahav](http://www.cs.technion.ac.il/~yahave/),
"code2vec: Learning Distributed Representations of Code", POPL'2019 [[PDF]](https://urialon.cswp.cs.technion.ac.il/wp-content/uploads/sites/83/2018/12/code2vec-popl19.pdf)

