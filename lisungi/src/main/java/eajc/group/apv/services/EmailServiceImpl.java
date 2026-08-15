package eajc.group.apv.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
public class EmailServiceImpl implements EmailService{

    private final JavaMailSender mailSender;
    private final String frontendUrl;

    public EmailServiceImpl(
            JavaMailSender mailSender,
            @Value("${app.frontend.url}") String frontendUrl) {

        this.mailSender = mailSender;
        this.frontendUrl = frontendUrl;
    }

    @Override
    public void sendResetEmail(String to, String token) {

        String resetLink = frontendUrl + "/reset-password?token=" + token;

        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(to);
        message.setSubject("Password Reset Request");
        message.setText(
                "To reset your password, click the link below:\n\n"
                        + resetLink
                        + "\n\nThis link will expire in 30 minutes."
        );

        mailSender.send(message);
    }
}
