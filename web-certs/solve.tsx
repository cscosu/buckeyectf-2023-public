import ReactPDF, {
  Document,
  Page,
  View,
  Text,
  StyleSheet,
} from "@react-pdf/renderer";
import * as jose from "jose";

const styles = StyleSheet.create({
  page: {
    flexDirection: "row",
    backgroundColor: "#E4E4E4",
  },
  section: {
    margin: 10,
    padding: 10,
    flexGrow: 1,
  },
});

const Certificate = ({ signature }: { signature: string }) => (
  <Document title="abc">
    <Page size="A4" style={styles.page} orientation="landscape">
      <View style={styles.section}>
        <Text>a</Text>
      </View>
      <View style={styles.section}>
        <Text>1</Text>
        <Text style={{ fontSize: 1 }}>{signature}</Text>
      </View>
    </Page>
  </Document>
);

const publicKey = new TextEncoder().encode(
  await Bun.file("public_key.pem").text()
);

const jwt = await new jose.SignJWT({ team: "a", place: 1 })
  .setProtectedHeader({ alg: "HS256" })
  .sign(publicKey);
console.log(jwt);

await ReactPDF.renderToFile(<Certificate signature={jwt} />, "solve.pdf");

const formData = new FormData();
formData.set("file", Bun.file("solve.pdf"));

const verify = await fetch("http://localhost:3001/api/verify", {
  method: "POST",
  body: formData,
});

// console.log(verify);
console.log(await verify.text());
