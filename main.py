from experiments import experiment, visual, save_to_excel

data = experiment()
save_to_excel(data)
visual(data)