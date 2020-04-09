from vocabularies import VocabType
from config import Config
from interactive_predict import InteractivePredictor
from model_base import Code2VecModelBase
import numpy as np
import os
import parser
import pickle
import csv

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
        number = 0
        for folder in range(2, 46):
            if folder == 16:
                continue
            knownSnippets = []
            print("folder", folder)
            np.set_printoptions(linewidth=np.inf)
            for root, dirs, files in os.walk('../BigCloneEval/ijadataset/bcb_reduced/' + str(folder)):
                for _file in files:
                    number+=1
                    filename = root + "/" + _file   
                    targetArray = predictor.getCodeVector(filename)
                    previousStart = 0
                    try:
                        for method in targetArray:
                            originalname, vec = method
                            vec = np.array(vec)
                            start, end = parser.findLines(filename, originalname, previousStart)
                            previousStart = start
                            _dir = root.split('/')[-1]
                            knownSnippets.append((_dir, _file, start, end, vec))
                    except Exception as e:
                        print(e)
                        print(_file)
                    print(number)

            with open("data" + str(folder) + ".csv", "w") as output:
                writer = csv.writer(output, delimiter=' ')
                writer.writerow([len(knownSnippets), len(knownSnippets[0][4])])
                for i in knownSnippets:
                    writer.writerow(i[0:4])
                    writer.writerow(i[4])


            print("csv for " + str(folder) + " folder uploaded")

    model.close_session()
