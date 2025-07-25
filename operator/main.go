package main

import (
	"context"
	"fmt"
	"log"
	"time"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/watch"
	"k8s.io/client-go/dynamic"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
)

var (
	gvr = schema.GroupVersionResource{
		Group:    "example.com",
		Version:  "v1",
		Resource: "myresources",
	}
)

func main() {
	log.Println("Starting basic operator...")

	// Get Kubernetes config
	config, err := getConfig()
	if err != nil {
		log.Fatalf("Failed to get config: %v", err)
	}

	// Create dynamic client
	client, err := dynamic.NewForConfig(config)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}

	// Start watching for resources
	watchResources(client)
}

func getConfig() (*rest.Config, error) {
	// Try in-cluster config first
	config, err := rest.InClusterConfig()
	if err != nil {
		// Fall back to kubeconfig
		config, err = clientcmd.BuildConfigFromFlags("", clientcmd.RecommendedHomeFile)
	}
	return config, err
}

func watchResources(client dynamic.Interface) {
	for {
		watcher, err := client.Resource(gvr).Watch(context.TODO(), metav1.ListOptions{})
		if err != nil {
			log.Printf("Failed to watch resources: %v", err)
			time.Sleep(10 * time.Second)
			continue
		}

		log.Println("Watching for MyResource events...")

		for event := range watcher.ResultChan() {
			obj, ok := event.Object.(*unstructured.Unstructured)
			if !ok {
				continue
			}

			switch event.Type {
			case watch.Added:
				log.Printf("Resource added: %s/%s", obj.GetNamespace(), obj.GetName())
				reconcile(client, obj)
			case watch.Modified:
				log.Printf("Resource modified: %s/%s", obj.GetNamespace(), obj.GetName())
				reconcile(client, obj)
			case watch.Deleted:
				log.Printf("Resource deleted: %s/%s", obj.GetNamespace(), obj.GetName())
			}
		}

		watcher.Stop()
		time.Sleep(5 * time.Second)
	}
}

func reconcile(client dynamic.Interface, obj *unstructured.Unstructured) {
	// Basic reconciliation logic
	name := obj.GetName()
	namespace := obj.GetNamespace()
	
	log.Printf("Reconciling resource: %s/%s", namespace, name)
	
	// Get desired state from spec
	spec, found, err := unstructured.NestedMap(obj.Object, "spec")
	if err != nil || !found {
		log.Printf("No spec found for resource %s/%s", namespace, name)
		return
	}
	
	// Simple example: ensure status reflects spec
	status := map[string]interface{}{
		"phase":   "Ready",
		"message": fmt.Sprintf("Resource %s is reconciled", name),
		"lastUpdated": time.Now().Format(time.RFC3339),
	}
	
	// Update status
	unstructured.SetNestedMap(obj.Object, status, "status")
	
	_, err = client.Resource(gvr).Namespace(namespace).UpdateStatus(context.TODO(), obj, metav1.UpdateOptions{})
	if err != nil {
		log.Printf("Failed to update status: %v", err)
	} else {
		log.Printf("Successfully reconciled %s/%s", namespace, name)
	}
}