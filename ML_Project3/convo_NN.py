__author__ = 'Admin'

from theano_classifier import *
from theano_convnet import *
from theano_utils import *
from features import *
from utils import *

# ------------------------
# Loading training set
# ------------------------
print "Loading train output..."
categories = loadnp("train_outputs.npy")
# print categories.shapes

print "Loading train input..."
examples = loadnp("train_inputs.mpy")

print "Loading test input..."
test_examples = loadnp("valid_inputs.npy")

test_categories = loadnp("valid_outputs.npy")

def contrast_normalize(x):
	min_x = min(x)
	max_x = max(x)
	res = (x - min_x)*1.0/(max_x - min_x)
	return np.array(res)

print "Doing contrast normalization..."
examples = map(contrast_normalize, examples)
examples = np.array(examples)
test_examples = map(contrast_normalize, test_examples)
test_examples = np.array(test_examples)

# # ------------------------
# # Getting test predictions
# # ------------------------
# print "Loading test input..."
# test_pred = loadnp("/Users/stephanielaflamme/Dropbox/COMP 598/Miniproject3/results/convnet_test_predictions.npy")[:20000]
# write_test_output(test_pred)


# -----------------
# VALIDATION
# ------------
print "Starting cross-validation..."

# Try to keep filter sizes 5-8
# At least 10 filters per layer
# 3 layers is good
# Only one hidden layer required
# 5000
#train_data, train_result = examples[5000:,:], categories[5000:]
#valid_data, valid_result = examples[:5000,:], categories[:5000]
#pad_test = np.zeros((20480, test_examples.shape[1]))
#pad_test[:20000] = test_examples
	# print "Generating new examples..."
	# new_data = map(lambda x,y: add_perturbation(x,y), train_data, train_result)
	# new_examples = np.asarray(map(lambda x: x[0], new_data))
	# new_outputs = np.asarray(map(lambda y: y[1], new_data))
	# print "Combining..."
	# train_input_expanded = np.asarray(zip(train_data, new_examples)).reshape((2*len(train_data), -1))
	# train_output_expanded = np.asarray(zip(train_result, new_outputs)).flatten()
	# np.save('train_inputs_expanded', train_input_expanded)
	# np.save('train_outputs_expanded', train_output_expanded)

print 'Building convnet...'
n_epochs = 750
batch_size = 512
learning_rate = 0.2
net = ConvNet(rng = np.random.RandomState(1234),
	# we're getting 720 instead of 320, why?
	# next image shape is (previous_image_shape - filter_size + 1) / poolsize
	# after  (20,1,7,7) images are (48-7+1 = 42) --> 21 x 21, then (21-6+1 = 16) --> 8x8
	# after (20, 1, 5, 5) images are (48-5+1 = 44) --> 22 x 22, then (22-5+1 = 18) --> 9x9, then...
	# (48-9+1=40) => 20x20, then (20-5+1 = 16)=> 8, then (8-5+1=4)=> 2
	# (48-7+1 = 42) => 21x21, then (21-6+1=16)=> 8x8, then (8-4+1=5)=> 5x5, and finally (5-3+1)=> 3x3
	# 21x21, then 16x16, (16-5+1=12) 12x12, (12-5+1=8)
	conv_filter_shapes = [(32, 1, 7, 7), (64, 32, 6, 6),(80, 64, 5, 5), (80,80,5,5)],#, [96, 80, 3, 3]], #(22, 22) output, shape ()
	image_shapes = [(batch_size, 1,48,48),(batch_size, 32, 21, 21), (batch_size, 64, 16, 16)],#, (batch_size, 80, 5, 5)], # (9, 9) output, shape (20,50,22,22) #80*2*2=320 but not getting that
	poolsizes=[(2,2),None, None,None],
	hidden_layer_sizes=[200],
	n_outputs=10,
	learning_rate=learning_rate,
	dropout_rate=0.5,
	activations=[rectified_linear],
	batch_size=batch_size,
	# train_set_x = train_input_expanded,
	# train_set_y = train_output_expanded,
	train_set_x=examples,
	train_set_y=categories,
	valid_set_x=test_examples,
	valid_set_y=test_categories
	# test_set = pad_test
	)
print 'Making the trainer...'
learner = Trainer(net)

print 'Training...'
best_val, best_val_pred = learner.train(learning_rate,n_epochs,batch_size)

print "Best validation error: %f" % best_val

np.save('timardeep', np.asarray(best_val_pred).flatten())
# np.save('/home/ml/slafla2/Miniproject-3/results/convnet_test_predictions', np.asarray(best_pred).flatten())


