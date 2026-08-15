package eajc.group.apv.repository;

import eajc.group.apv.entity.Donation;
import eajc.group.apv.entity.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface DonationRepository extends JpaRepository<Donation, Long> {

    Optional<Donation> findByPublicId(UUID publicId);

    List<Donation> findByBeneficiaryId(Long beneficiaryId);

    boolean existsByBeneficiaryIdAndTitle(Long beneficiaryId, String title);

    boolean existsByBeneficiaryIdAndTitleAndPublicIdNot(Long beneficiaryId, String title, UUID publicId);

    List<Donation> findByDateDonationBetween(
            LocalDate startDate,
            LocalDate endDate
    );

    @Query("""
            SELECT YEAR(dateDonation), COUNT(d)
            FROM Donation d
            GROUP BY YEAR(d.dateDonation)
            ORDER BY YEAR(d.dateDonation)
        """)
    List<Object[]> countDonationsByYear();

    @Query("""
        SELECT d.beneficiary.id, d.beneficiary.publicId, d.beneficiary.name, d.beneficiary.type, COUNT(d)
        FROM Donation d
        GROUP BY d.beneficiary.id, d.beneficiary.publicId, d.beneficiary.name, d.beneficiary.type
    """)
    List<Object[]> countDonationsByBeneficiary();
}
