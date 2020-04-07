# Code2vec model for clone detecting  
This is my technical work for JetBrains internship.

In this work I used code2vec model described in [1] and implemented in [2].

The main idea of the vector representation is that code snippets with the same meaning will mapped to simular vectors (respect Euclidean metric).

Then I specified threshold (in my case I hardcoded it on 60).
If distance between vectors will be smaller thus I consider that they are clones.


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
Step 4: Initialize the tools 
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
./registerTool -n "code2vec" -d "60 threshold"
```



### Step 5: Evaluating a trained model
Suppose that iteration #8 is our chosen model, run from JB-application directory:
```
python3 code2vec.py --load models/java14_model/saved_model_iter8.release --predict --export_code_vectors
```
While evaluating, a number of files named "data<N>.csv" is written with each pair of clones in the following format:
```
<total number of snippets> <dimension of code vector>
```
Then 'rows' times:
```
<dirname1> <filename1> <line start 1>,<line end 1>,<dirname2>,<filename2>,<line start 2>,<line end 2>
```

## import clones
Go to the commands directory of BigCloneEval distribution and run: 
```
./importClones -t 1 -c ../../JB-application/code2vec.clones
```
after importing run
```
./evaluateTool -t 1 -o code2vec.report
```
It will generate you report about your tool.

My model still evaluating.
Precision and recall will appear here approximately in 1 day.

## Citation

[1] [code2vec: Learning Distributed Representations of Code](https://urialon.cswp.cs.technion.ac.il/wp-content/uploads/sites/83/2018/12/code2vec-popl19.pdf)
[2] github.com/tech-srl/code2vec

[Uri Alon](http://urialon.cswp.cs.technion.ac.il), [Meital Zilberstein](http://www.cs.technion.ac.il/~mbs/), [Omer Levy](https://levyomer.wordpress.com) and [Eran Yahav](http://www.cs.technion.ac.il/~yahave/),
"code2vec: Learning Distributed Representations of Code", POPL'2019 [[PDF]](https://urialon.cswp.cs.technion.ac.il/wp-content/uploads/sites/83/2018/12/code2vec-popl19.pdf)

