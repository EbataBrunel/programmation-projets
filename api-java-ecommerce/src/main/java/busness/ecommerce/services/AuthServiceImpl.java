package busness.ecommerce.services;

import busness.ecommerce.dto.ForgotPasswordRequestDto;
import busness.ecommerce.dto.ResetPasswordRequestDto;
import busness.ecommerce.entity.PasswordResetToken;
import busness.ecommerce.entity.User;
import busness.ecommerce.repository.PasswordResetTokenRepository;
import busness.ecommerce.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService{

    private final UserRepository userRepository;
    private final PasswordResetTokenRepository tokenRepository;
    private final PasswordEncoder passwordEncoder;
    private final EmailService emailService;

    @Override
    public void forgotPassword(ForgotPasswordRequestDto request) {
        Optional<User> optionalUser = userRepository.findByEmail(request.getEmail());

        if (optionalUser.isEmpty()) {
            return; // sécurité : on ne révèle pas si l'email existe
        }

        User user = optionalUser.get();

        String token = UUID.randomUUID().toString();

        PasswordResetToken resetToken = tokenRepository.findByUser(user)
                        .orElse(new PasswordResetToken());

        resetToken.setToken(token);
        resetToken.setUser(user);
        resetToken.setExpirationDate(LocalDateTime.now().plusMinutes(30));

        tokenRepository.save(resetToken);

        emailService.sendResetEmail(user.getEmail(), token);
    }

    @Override
    public void resetPassword(ResetPasswordRequestDto request) {
        PasswordResetToken resetToken =
                tokenRepository.findByToken(request.getToken())
                        .orElseThrow(() -> new RuntimeException("Invalid token"));

        if (resetToken.getExpirationDate().isBefore(LocalDateTime.now())) {
            throw new RuntimeException("Token expired");
        }

        User user = resetToken.getUser();
        user.setPassword(
                passwordEncoder.encode(request.getNewPassword())
        );

        userRepository.save(user);

        tokenRepository.delete(resetToken);
    }
}
