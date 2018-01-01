from django.shortcuts import render

# Create your views here.
def index(request):
	if 'Load_Map_id' in request.POST.keys():
		print ("Load_Map_id :{} ".format(request.POST['Load_Map_id'] ) ) 	
	
	if 'Save_Map_id' in request.POST.keys():
		print ("Save_Map_id :{} ".format(request.POST['Save_Map_id'] ) ) 	
	
	
	if 'Add_Node_id' in request.POST.keys():
		print ("Add_Node_id :{} ".format(request.POST['Add_Node_id'] ) ) 
	
	
	if 'Add_Node_x' in request.POST.keys():
		print ("Add_Node_x :{} ".format(request.POST['Add_Node_x'] ) )

	
	if 'Add_Node_y' in request.POST.keys():
		print ("Add_Node_y :{} ".format(request.POST['Add_Node_y'] ) )

	
	if 'Add_Edge_from' in request.POST.keys():
		print ("Add_Edge_from :{} ".format(request.POST['Add_Edge_from'] ) ) 


	if 'Del_Node_id' in request.POST.keys():
		print ("Del_Node_id :{} ".format(request.POST['Del_Node_id'] ) ) 
	
	
	if 'Add_Edge_from' in request.POST.keys():
		print ("Add_Edge_from :{} ".format(request.POST['Add_Edge_from'] ) ) 


	if 'Add_Edge_to' in request.POST.keys():
		print ("Add_Edge_to :{} ".format(request.POST['Add_Edge_to'] ) )

	if 'Del_Edge_from' in request.POST.keys():
		print ("Del_Edge_from :{} ".format(request.POST['Del_Edge_from'] ) ) 


	if 'Del_Edge_to' in request.POST.keys():
		print ("Del_Edge_to :{} ".format(request.POST['Del_Edge_to'] ) )


	if 'Gen_no' in request.POST.keys():
		print ("Generator Number : {} ".format(request.POST['Gen_no'] ) )

	
	if 'CarStats' in request.POST.keys():
		print ("Debug_level :{} ".format(request.POST['CarStats'] ) )

	if 'EdgeStats' in request.POST.keys():
		print ("Debug_level :{} ".format(request.POST['EdgeStats'] ) )

	if 'CarEnterExits' in request.POST.keys():
		print ("Debug_level :{} ".format(request.POST['CarEnterExits'] ) )
    
	context = {
        'message': 'Hello'
    }
	return render(request, 'sim_app/index.html', context)
def simulation(request):
	return render(request, 'sim_app/simulation.html', {})
