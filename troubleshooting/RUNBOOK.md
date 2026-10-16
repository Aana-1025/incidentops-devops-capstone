# Kubernetes Troubleshooting Runbook

These exercises are intentionally isolated from the Helm-managed IncidentOps resources. Run them only in the local `incidentops` namespace, capture evidence manually when required, and delete each demo before continuing.

## Broken image

**Symptom:** the demo Pod reaches `ErrImagePull` and then `ImagePullBackOff` while the real application remains healthy.

```powershell
kubectl apply -f .\troubleshooting\broken-image.yaml
kubectl get pods -n incidentops -l incidentops.io/scenario=broken-image
kubectl describe pod -n incidentops -l incidentops.io/scenario=broken-image
kubectl get events -n incidentops --sort-by=.metadata.creationTimestamp
```

**Investigation:** `get` identifies the waiting state. `describe` and the namespace events show that Kubernetes cannot pull the deliberately nonexistent `troubleshooting-does-not-exist` tag.

**Root cause:** the Deployment references an invalid container image tag.

**Fix and verification:** copy the immutable image already used by the healthy backend, update only the demo Deployment, and wait for its Pod to become Ready.

```powershell
$validImage = kubectl get deployment incidentops-backend -n incidentops `
  -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl set image deployment/incidentops-broken-image-demo `
  -n incidentops demo=$validImage
kubectl rollout status deployment/incidentops-broken-image-demo `
  -n incidentops --timeout=3m
kubectl get pods -n incidentops -l incidentops.io/scenario=broken-image
kubectl delete -f .\troubleshooting\broken-image.yaml
```

## Wrong Service target port

**Symptom:** the demo Pod is Ready and directly serves HTTP on port `8080`, but traffic through its Service fails because the Service forwards to port `9999`.

```powershell
kubectl apply -f .\troubleshooting\wrong-target-port.yaml
kubectl rollout status deployment/incidentops-wrong-service-demo `
  -n incidentops --timeout=3m
kubectl get pods,svc -n incidentops -l incidentops.io/scenario=wrong-target-port
kubectl describe service incidentops-wrong-service-demo -n incidentops
kubectl get endpointslice -n incidentops `
  -l kubernetes.io/service-name=incidentops-wrong-service-demo -o yaml
kubectl get pod -n incidentops -l incidentops.io/scenario=wrong-target-port `
  -o jsonpath='{.items[0].spec.containers[0].ports[0].containerPort}'
kubectl run incidentops-service-client -n incidentops --rm -i --restart=Never `
  --image=curlimages/curl:8.23.0 -- `
  curl -fsS --max-time 5 http://incidentops-wrong-service-demo/
```

**Investigation:** the Deployment shows container port `8080`, while the Service and EndpointSlice show target port `9999`. The selected Pod is healthy, so the mismatch—not labels or application startup—is the cause.

**Root cause:** the Service forwards to a port where the application is not listening.

**Fix and verification:** patch the demo Service to the actual container port, repeat the request, then remove both demo resources.

```powershell
kubectl patch service incidentops-wrong-service-demo -n incidentops `
  --type merge -p '{"spec":{"ports":[{"name":"http","port":80,"targetPort":8080}]}}'
kubectl run incidentops-service-client -n incidentops --rm -i --restart=Never `
  --image=curlimages/curl:8.23.0 -- `
  curl -fsS --max-time 10 http://incidentops-wrong-service-demo/
kubectl delete -f .\troubleshooting\wrong-target-port.yaml
```

## Final safety check

```powershell
kubectl get pods,deployments,svc,hpa -n incidentops
kubectl get all -n incidentops -l app.kubernetes.io/part-of=incidentops-troubleshooting
```

The second command must return no resources. Confirm two Ready frontend replicas, two Ready backend replicas after HPA stabilization, one Ready PostgreSQL Pod, working `/health` and `/ready`, and no test records before ending the demo.
