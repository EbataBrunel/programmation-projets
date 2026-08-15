package eajc.group.apv.repository;

import eajc.group.apv.entity.User;
import eajc.group.apv.entity.UserProfile;
import eajc.group.apv.enums.Reason;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface UserProfileRepository extends JpaRepository<UserProfile, Long> {
    UserProfile findByUser(User user);
    Optional<UserProfile> findByPublicId(UUID publicId);
    List<UserProfile> findByRegistrationDate(LocalDate registrationDate);
    List<UserProfile> findByReasonRemovalNot(Reason reasonRemoval);

    @Query("""
        SELECT p.gender, COUNT(p)
        FROM UserProfile p
        WHERE p.gender IS NOT NULL
        GROUP BY p.gender
    """)
        List<Object[]> countProfilesByGender();
}
