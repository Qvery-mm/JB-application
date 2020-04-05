from vocabularies import VocabType
from config import Config
from interactive_predict import InteractivePredictor
from model_base import Code2VecModelBase
import numpy as np
import os
import parser


def load_model_dynamically(config: Config) -> Code2VecModelBase:
    assert config.DL_FRAMEWORK in {'tensorflow', 'keras'}
    if config.DL_FRAMEWORK == 'tensorflow':
        from tensorflow_model import Code2VecModel
    elif config.DL_FRAMEWORK == 'keras':
        from keras_model import Code2VecModel
    return Code2VecModel(config)


if __name__ == '__main__':
    config = Config(set_defaults=True, load_from_args=True, verify=True)

    model = load_model_dynamically(config)
    config.log('Done creating code2vec model')

    if config.is_training:
        model.train()
    if config.SAVE_W2V is not None:
        model.save_word2vec_format(config.SAVE_W2V, VocabType.Token)
        config.log('Origin word vectors saved in word2vec text format in: %s' % config.SAVE_W2V)
    if config.SAVE_T2V is not None:
        model.save_word2vec_format(config.SAVE_T2V, VocabType.Target)
        config.log('Target word vectors saved in word2vec text format in: %s' % config.SAVE_T2V)
    if (config.is_testing and not config.is_training) or config.RELEASE:
        eval_results = model.evaluate()
        if eval_results is not None:
            config.log(
                str(eval_results).replace('topk', 'top{}'.format(config.TOP_K_WORDS_CONSIDERED_DURING_PREDICTION)))
    if config.PREDICT:
        predictor = InteractivePredictor(config, model)

        with open("code2vecClones", "w") as output:
            maxn = 5
            np.set_printoptions(linewidth=np.inf)
            for root, dirs, files in os.walk('/home/aleksandr/Documents/JetBrains/BigCloneEval/ijadataset/bcb_reduced/2'):
                for _file in files:
                    filename = root + "/" + _file   
                    #print(filename)
                    targetArray = predictor.getCodeVector(filename)
                    previousStart = 0
                    for method in targetArray:
                        originalname, vec = method
                        vec = np.array(vec)
                        start, end = parser.findLines(filename, originalname, previousStart)
                        previousStart = start
                        print(originalname, start, end, _file, file=output) #TODO add vec to output
                    #print(filename, vec)
                    maxn -= 1
                    if maxn <= 0:
                        break
		#predictor.predict()
		#vec1 = np.array(predictor.getCodeVector("Input.java"))
		#vec2 = np.array(predictor.getCodeVector("Input-second.java"))
		#print(vec1)
		#subs = vec1 - vec2
		#print(subs)
		#print(np.matmul(subs, subs))
    model.close_session()
