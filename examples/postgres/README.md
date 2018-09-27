# A simple web application deployment example 

If you run the command below it will render the k8s yaml file that then can be used with `kubectl` for example.

    kuku render -f values.yaml templates/
    
The dot at the end is the path where the `templates` dir is located.
    
You can then use the output of `kuku render` to apply the changes against your k8s cluster:

    kuku render -f values.yaml templates/ | kubectl apply -f -
    
    
You can also apply the changes directly:

    kuku apply -f values.yaml templates/


To delete the resources created:

    kuku delete -f values.yaml templates/
    
    
Behind the scenes `apply` and `delete` are using `kubectl apply` and `kubectl delete`.

Pretty often you also want to have different values for production/staging environments.
Here's how you can customize your output:

    kuku apply -f values.yaml -f values-prod.yaml -s env=prod,replicas=3 templates/
