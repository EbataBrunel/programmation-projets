package eajc.group.apv.services;

public interface EmailService {
    void sendResetEmail(String to, String token);
}
