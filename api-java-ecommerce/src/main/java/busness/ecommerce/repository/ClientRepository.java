package busness.ecommerce.repository;

import busness.ecommerce.entity.User;
import busness.ecommerce.entity.UserProfile;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClientRepository extends JpaRepository<UserProfile, Long> {
    UserProfile findByUser(User user);
}
