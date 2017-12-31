from django.shortcuts import render

def index(request):
	
	if 'Map_id' in request.POST.keys():
		print ("Map_id :{} ".format(request.POST['Map_id'] ) ) 	
	
	
	if 'Node_id' in request.POST.keys():
		print ("Node_id :{} ".format(request.POST['Node_id'] ) ) 
	
	
	if 'Node_x' in request.POST.keys():
		print ("Node_x :{} ".format(request.POST['Node_x'] ) )

	
	if 'Node_y' in request.POST.keys():
		print ("Node_y :{} ".format(request.POST['Node_y'] ) )

	
	if 'Edge_id' in request.POST.keys():
		print ("Edge_id :{} ".format(request.POST['Edge_id'] ) ) 


	if 'Edge_from' in request.POST.keys():
		print ("Edge_from :{} ".format(request.POST['Edge_from'] ) ) 


	if 'Edge_to' in request.POST.keys():
		print ("Edge_to :{} ".format(request.POST['Edge_to'] ) )


	if 'Gen_no' in request.POST.keys():
		print ("Generator Number : {} ".format(request.POST['Gen_no'] ) )

	
	if 'CarStats' in request.POST.keys():
		print ("Debug_level :{} ".format(request.POST['CarStats'] ) )

	if 'EdgeStats' in request.POST.keys():
		print ("Debug_level :{} ".format(request.POST['EdgeStats'] ) )

	if 'CarEnterExits' in request.POST.keys():
		print ("Debug_level :{} ".format(request.POST['CarEnterExits'] ) )

	return render(request, 'index.html', {})

def simulation(request):
	if 'Tickperiod' in request.POST.keys():
		print("Tickperiof of Simulation {}".format(request.POST['Tickperiod']) )
	print("simulatiın function")
	return render(request , 'simulation.html',{})
