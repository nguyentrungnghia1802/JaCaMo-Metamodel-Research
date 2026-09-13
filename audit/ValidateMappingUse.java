import java.io.*;
import java.nio.file.*;
import org.tzi.use.parser.use.USECompiler;
import org.tzi.use.uml.mm.*;

/** Compile declarations only. Never constructs MSystem/MSystemState or objects. */
class ValidateMappingUse {
    public static void main(String[] args) throws Exception {
        StringWriter diagnostics=new StringWriter();
        MModel model;
        try (InputStream stream=Files.newInputStream(Path.of(args[0]))) {
            model=USECompiler.compileSpecification(stream,args[0],new PrintWriter(diagnostics),new ModelFactory());
        }
        if(args[1].startsWith("reject")) {
            if(model!=null) throw new IllegalStateException("Negative control unexpectedly compiled");
            boolean expected=args[1].equals("reject")
                ? diagnostics.toString().contains("conflicts with same rolename")
                : diagnostics.toString().contains("no viable alternative") || diagnostics.toString().contains("mismatched input");
            if(!expected)
                throw new IllegalStateException("Unexpected rejection: "+diagnostics);
            System.out.println("PASS: "+(args[1].equals("reject") ? "reverse-role collision" : "reserved identifier")+" rejected by USE");
            return;
        }
        if(model==null || !diagnostics.toString().isBlank())
            throw new IllegalStateException("USE compilation failed/warned: "+diagnostics);
        int attrs=0,parents=0,orderedEnds=0,operations=0;
        for(MClass c:model.classes()) {attrs+=c.attributes().size();parents+=c.parents().size();operations+=c.operations().size();}
        for(MAssociation a:model.associations())
            for(MAssociationEnd e:a.associationEnds()) if(e.isOrdered()) orderedEnds++;
        int[] actual={model.classes().size(),attrs,model.associations().size(),parents,orderedEnds,operations};
        for(int i=0;i<actual.length;i++)
            if(actual[i]!=Integer.parseInt(args[i+2])) throw new IllegalStateException("Count mismatch index "+i+": "+actual[i]);
        System.out.println("PASS: USE declarations classes="+actual[0]+" attributes="+attrs+" associations="+actual[2]+" inheritance="+parents+" orderedEnds="+orderedEnds+" operations="+operations);
    }
}
