package eajc.group.apv.services;

import eajc.group.apv.dto.ChangePasswordRequest;
import eajc.group.apv.dto.ForgotPasswordRequest;
import eajc.group.apv.dto.ResetPasswordRequest;
import eajc.group.apv.entity.PasswordResetToken;
import eajc.group.apv.entity.User;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.repository.PasswordResetTokenRepository;
import eajc.group.apv.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
@Transactional
public class PasswordRestServiceImpl implements PasswordResetService{

    private final UserRepository userRepository;
    private final PasswordResetTokenRepository tokenRepository;
    private final PasswordEncoder passwordEncoder;
    private final EmailService emailService;

    public PasswordRestServiceImpl(UserRepository userRepository, PasswordResetTokenRepository tokenRepository, PasswordEncoder passwordEncoder, EmailService emailService) {
        this.userRepository = userRepository;
        this.tokenRepository = tokenRepository;
        this.passwordEncoder = passwordEncoder;
        this.emailService = emailService;
    }


    @Override
    public void forgotPassword(ForgotPasswordRequest request) {
        userRepository.findByEmail(request.getEmail())
                .ifPresent(user -> {

                    PasswordResetToken resetToken = tokenRepository.findByUser(user)
                            .orElse(new PasswordResetToken());

                    resetToken.setUser(user);
                    resetToken.setToken(UUID.randomUUID().toString());
                    resetToken.setExpirationDate(LocalDateTime.now().plusMinutes(30));

                    tokenRepository.save(resetToken);

                    emailService.sendResetEmail(user.getEmail(), resetToken.getToken());

                });
    }

    @Override
    public void resetPassword(ResetPasswordRequest request) {
        PasswordResetToken token = tokenRepository.findByToken(request.getToken())
                .orElseThrow(() -> new IllegalArgumentException("Token invalide"));

        if(token.getExpirationDate().isBefore(LocalDateTime.now())){
            throw new IllegalArgumentException("Le lien a expiré");
        }

        User user = token.getUser();

        user.setPassword(passwordEncoder.encode(request.getPassword()));

        userRepository.save(user);

        tokenRepository.delete(token);
    }

    @Override
    public void changePassword(String username, ChangePasswordRequest request) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        // Vérification de l'ancien mot de passe
        if (!passwordEncoder.matches(request.getOldPassword(), user.getPassword())) {
            throw new BadRequestException("Ancien mot de passe incorrect");
        }

        // Vérification de la confirmation
        if (!request.getNewPassword().equals(request.getConfirmPassword())) {
            throw new BadRequestException("Les mots de passe ne correspondent pas");
        }

        // Vérification qu'il est différent de l'ancien
        if (passwordEncoder.matches(request.getNewPassword(), user.getPassword())) {
            throw new BadRequestException("Le nouveau mot de passe doit être différent");
        }

        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        userRepository.save(user);
    }
}
