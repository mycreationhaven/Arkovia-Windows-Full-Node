import java.net.URI;
import java.net.HttpURLConnection;
import java.nio.charset.StandardCharsets;
import java.util.Properties;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import nxt.Nxt;

/** Exercises the compiled node with an isolated, disposable database. */
public final class NodeSmokeTest {
    private static String get(String path) throws Exception {
        HttpURLConnection connection = (HttpURLConnection)
            URI.create("http://127.0.0.1:4876/" + path).toURL().openConnection();
        connection.setConnectTimeout(10000);
        connection.setReadTimeout(10000);
        try {
            if (connection.getResponseCode() != 200) {
                throw new IllegalStateException("HTTP " + connection.getResponseCode());
            }
            return new String(connection.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        } finally { connection.disconnect(); }
    }

    public static void main(String[] args) throws Exception {
        if (args.length > 0 && args[0].equals("windows") &&
            (!System.getProperty("os.name").startsWith("Windows") ||
             !System.getProperty("os.arch").equals("amd64"))) {
            throw new IllegalStateException("Expected a Windows AMD64 runtime");
        }
        Properties testOnly = new Properties();
        testOnly.setProperty("nxt.isOffline", "true");
        // No live peer traffic or keys are needed for the startup check.
        // The distributed nxt.properties is left unchanged.
        try {
            Nxt.init(testOnly);
            JSONObject status = (JSONObject) JSONValue.parse(get("nxt?requestType=getBlockchainStatus"));
            if (!"Arkovia".equals(status.get("application")) ||
                !"1.13.1".equals(status.get("version")) ||
                !Boolean.FALSE.equals(status.get("isLightClient")) ||
                !Boolean.FALSE.equals(status.get("isTestnet")) ||
                !Boolean.FALSE.equals(status.get("apiProxy"))) {
                throw new IllegalStateException("Unexpected node status: " + status);
            }
            JSONObject block = (JSONObject) JSONValue.parse(get("nxt?requestType=getBlock&height=0"));
            if (!"10203308059164672611".equals(block.get("block"))) {
                throw new IllegalStateException("Unexpected genesis: " + block);
            }
            String wallet = get("");
            if (wallet.length() < 1000 || !wallet.toLowerCase().contains("<html")) {
                throw new IllegalStateException("Wallet HTML missing");
            }
            System.out.println("SMOKE_PASS " + status.toJSONString());
        } finally {
            Nxt.shutdown();
        }
    }
}
