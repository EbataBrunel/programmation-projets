package eajc.group.apv.repository;

import eajc.group.apv.entity.Beneficiary;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface   BeneficiaryRepository extends JpaRepository<Beneficiary, Long> {
    Optional<Beneficiary> findByPublicId(UUID publicId);
    boolean existsByPhoneAndNameIgnoreCase(String phone, String name);
    boolean existsByPhoneAndNameIgnoreCaseAndPublicIdNot(String phone, String name, UUID publicId);
}
