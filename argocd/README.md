# Local Argo CD GitOps Demonstration

This application is a final local GitOps supplement. It watches the public IncidentOps repository, renders `helm/incidentops` with `values-gitops.yaml`, and reconciles the result into the isolated `incidentops-gitops` namespace on Docker Desktop Kubernetes.

The demonstration deliberately does not manage the existing `incidentops` namespace or historical M10 Helm release. Ingress, HPA, and ServiceMonitor creation are disabled for this copy so it cannot conflict with the verified local release or monitoring stack. Both application images remain pinned to the M10 release SHA.

Argo CD itself is installed from the pinned official `v3.5.5` manifest in the `argocd` namespace. Apply `application.yaml` only while `kubectl config current-context` is `docker-desktop`.

```powershell
kubectl config current-context
kubectl apply -f .\argocd\application.yaml
kubectl get applications.argoproj.io -n argocd incidentops-gitops
kubectl get pods -n incidentops-gitops
```

The Application uses automated synchronization with pruning and self-healing, scoped only to `incidentops-gitops`.
