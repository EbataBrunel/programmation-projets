package eajc.group.apv.repository;

import eajc.group.apv.entity.PasswordResetToken;
import eajc.group.apv.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface PasswordResetTokenRepository extends JpaRepository<PasswordResetToken, Long> {
    Optional<PasswordResetToken> findByToken(String token);

    Optional<PasswordResetToken> findByUser(User user);

    void deleteByToken(String token);

    void deleteByUser(User user);
}
