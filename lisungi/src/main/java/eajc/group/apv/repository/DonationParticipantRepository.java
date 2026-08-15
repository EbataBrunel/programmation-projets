package eajc.group.apv.repository;

import eajc.group.apv.entity.DonationParticipant;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface DonationParticipantRepository extends JpaRepository<DonationParticipant, Long> {
    Optional<DonationParticipant> findByPublicId(UUID publicId);
    List<DonationParticipant> findByDonationId(Long donationId);
    boolean existsByDonationIdAndName(Long donationId, String name);
    boolean existsByDonationIdAndNameAndPublicIdNot(Long donationId, String name, UUID publicId);

    @Query("""
        SELECT 
            d.beneficiary.id,
            d.beneficiary.publicId,
            d.beneficiary.name,
            COUNT(DISTINCT d.id)
        FROM Donation d
        JOIN d.participants p
        GROUP BY 
            d.beneficiary.id,
            d.beneficiary.publicId,
            d.beneficiary.name
    """)
    List<Object[]> countDonationByBeneficiaryWithParticipant();

    @Query("""
        SELECT
            p.donation.id,
            p.donation.publicId,
            p.donation.title,
            p.donation.closure_status,
            COUNT(p)
        FROM DonationParticipant p
        WHERE p.donation.beneficiary.publicId = :beneficiaryPublicId
        GROUP BY p.donation.id, p.donation.publicId, p.donation.title, p.donation.closure_status
    """)
    List<Object[]> countParticipantsByDonationAndBeneficiary(
            @Param("beneficiaryPublicId") UUID beneficiaryPublicId
    );
}
