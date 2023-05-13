import NeuralNetwork
from time import perf_counter
save_model = 'C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\models\\model_weights_HP.hdf5'
path = 'C:\\Users\\Dantalyan\\Desktop\\Future\\appNeyronetwork\\Data_set\\HP.txt'

start=perf_counter()
neur = NeuralNetwork.Neyron(150, save_model, '', path)
neur.Load_Model()
print(neur.Set_text(1.2))
end =perf_counter()
print(end-start)

