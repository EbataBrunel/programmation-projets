package busness.ecommerce.services;

public interface EmailService {
    void sendResetEmail(String to, String token);
}
