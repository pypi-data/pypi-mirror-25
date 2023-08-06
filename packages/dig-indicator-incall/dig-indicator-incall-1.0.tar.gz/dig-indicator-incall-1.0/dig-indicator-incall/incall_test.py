import pickle
import fasttext
from numpy import array





if __name__ == "__main__":
    # #load pre-trained fasttext bin model
    model = fasttext.load_model('./model//fasttext_vec20_model.bin')

    text = raw_input("Input:")
    text_vector = array(model[text])
    vector_array = text_vector.reshape(1, -1) # it is a single sample

    #load pre-trained model
    filename = './model/incall_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    if loaded_model.predict(vector_array) == 1.:
        print True
    else:
        print False






#
# # result = loaded_model.predict(vector)
# # print result

