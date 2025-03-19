import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class PasswordEncryptor {
    private static final String SECRET_KEY = "MySuperSecretKey"; // Must be 16 characters
    private static final String ALGORITHM = "AES";

    // Encrypt Password
    public static String encrypt(String password) throws Exception {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        SecretKeySpec secretKey = new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] encrypted = cipher.doFinal(password.getBytes());
        return Base64.getEncoder().encodeToString(encrypted);  // Correct Base64 encoding
    }

    // Decrypt Password
    public static String decrypt(String encryptedPassword) throws Exception {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        SecretKeySpec secretKey = new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        
        byte[] decodedBytes = Base64.getDecoder().decode(encryptedPassword);  // Correct Base64 decoding
        byte[] decryptedBytes = cipher.doFinal(decodedBytes);
        return new String(decryptedBytes);
    }

    // Main CLI
    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.out.println("Usage: java -cp passwordencryptor.jar PasswordEncryptor <encrypt/decrypt> <password>");
            return;
        }

        String command = args[0];
        String input = args[1];

        if (command.equalsIgnoreCase("encrypt")) {
            System.out.println("Encrypted Password: " + encrypt(input));
        } else if (command.equalsIgnoreCase("decrypt")) {
            System.out.println("Decrypted Password: " + decrypt(input));
        } else {
            System.out.println("Invalid command. Use 'encrypt' or 'decrypt'.");
        }
    }
}
