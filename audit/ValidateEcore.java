import java.nio.file.*;
import java.util.*;
import org.eclipse.emf.common.util.*;
import org.eclipse.emf.ecore.*;
import org.eclipse.emf.ecore.resource.*;
import org.eclipse.emf.ecore.resource.impl.*;
import org.eclipse.emf.ecore.xmi.impl.*;
import org.eclipse.emf.ecore.util.*;

public class ValidateEcore {
  static void printDiagnostic(Diagnostic d, String indent) {
    System.out.println(indent+"severity="+d.getSeverity()+" source="+d.getSource()+" code="+d.getCode()+" "+d.getMessage());
    for (Diagnostic c : d.getChildren()) printDiagnostic(c,indent+"  ");
  }
  public static void main(String[] args) throws Exception {
    ResourceSet rs=new ResourceSetImpl();
    rs.getResourceFactoryRegistry().getExtensionToFactoryMap().put("ecore",new EcoreResourceFactoryImpl());
    rs.getPackageRegistry().put(EcorePackage.eNS_URI,EcorePackage.eINSTANCE);
    Resource r=rs.getResource(URI.createFileURI(Paths.get(args[0]).toAbsolutePath().toString()),true);
    EcoreUtil.resolveAll(rs);
    System.out.println("resource.errors="+r.getErrors().size()+" resource.warnings="+r.getWarnings().size());
    for (Resource.Diagnostic d:r.getErrors()) System.out.println("LOAD ERROR: "+d);
    var unresolved=EcoreUtil.UnresolvedProxyCrossReferencer.find(rs);
    System.out.println("unresolved.proxies="+unresolved.size());
    int severity=0,classes=0,attributes=0,references=0,generalizations=0;
    for (EObject o:r.getContents()) {
      Diagnostic d=Diagnostician.INSTANCE.validate(o); printDiagnostic(d,""); severity=Math.max(severity,d.getSeverity());
      if(o instanceof EPackage p) {
        for(EClassifier classifier:p.getEClassifiers()) if(classifier instanceof EClass c) {
          classes++; generalizations+=c.getESuperTypes().size();
          for(EStructuralFeature f:c.getEStructuralFeatures()) {
            if(f instanceof EAttribute) attributes++; else if(f instanceof EReference) references++;
          }
        }
        EClass message=(EClass)p.getEClassifier("Message");
        EAttribute broadcast=(EAttribute)message.getEStructuralFeature("isBroadcast");
        System.out.println("Message.isBroadcast.defaultValueLiteral="+broadcast.getDefaultValueLiteral()+" effectiveDefault="+broadcast.getDefaultValue());
        EClass scheme=(EClass)p.getEClassifier("Scheme");
        System.out.println("Scheme.inherited.id.owner="+scheme.getEStructuralFeature("id").getEContainingClass().getName());
        EClass norm=(EClass)p.getEClassifier("Norm");
        System.out.println("Norm.inherited.normativespecification.containment="+((EReference)norm.getEStructuralFeature("normativespecification")).isContainment());
      }
    }
    System.out.println("classes="+classes+" attributes="+attributes+" references="+references+" generalizations="+generalizations);
    if(severity>=Diagnostic.ERROR || !r.getErrors().isEmpty() || !unresolved.isEmpty()) System.exit(1);
  }
}
