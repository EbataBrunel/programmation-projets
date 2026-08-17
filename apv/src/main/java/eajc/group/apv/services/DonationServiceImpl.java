package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import eajc.group.apv.entity.Donation;
import eajc.group.apv.entity.Beneficiary;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.DonationMapper;
import eajc.group.apv.repository.DonationRepository;
import eajc.group.apv.repository.BeneficiaryRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.LocalDate;
import java.time.Year;
import java.time.YearMonth;
import java.util.List;
import java.util.UUID;

@Service
public class DonationServiceImpl implements DonationService {

    private final DonationRepository donationRepository;
    private final DonationMapper donationMapper;
    private final BeneficiaryRepository beneficiaryRepository;
    private final FileStorageService fileStorageService;

    public DonationServiceImpl(DonationRepository donationRepository, DonationMapper donationMapper, BeneficiaryRepository beneficiaryRepository, FileStorageService fileStorageService) {
        this.donationRepository = donationRepository;
        this.donationMapper = donationMapper;
        this.beneficiaryRepository = beneficiaryRepository;
        this.fileStorageService = fileStorageService;
    }


    @Override
    public DonationResponseDto createDonation(DonationRequestDto dto, MultipartFile photoFile) throws IOException {
        if (dto.getTitle() == null || dto.getTitle().trim().isEmpty()) {
            throw new BadRequestException("Le titre est obligatoire.");
        }

        if (dto.getDescription() == null || dto.getDescription().trim().isEmpty()) {
            throw new BadRequestException("La description est obligatoire.");
        }

        if (dto.getDateDonation() == null) {
            throw new BadRequestException("La date est obligatoire.");
        }

        Beneficiary beneficiary = beneficiaryRepository.findById(dto.getBeneficiaryId())
                .orElseThrow(() -> new ResourceNotFoundException("Bnéficiaire introuvale"));


        // Vérification doublon Beneficiary + Title
        if (donationRepository.existsByBeneficiaryIdAndTitle(
                beneficiary.getId(),
                dto.getTitle().trim()
        )) {
            throw new BadRequestException(
                    "Ce bénéficiaire est déjà associé à ce titre de don."
            );
        }

        String fileName = fileStorageService.saveFile(photoFile);

        Donation donation = donationMapper.toEntity(dto, beneficiary, fileName);
        Donation donationSave = donationRepository.save(donation);
        return donationMapper.toDto(donationSave);
    }

    @Override
    public List<DonationResponseDto> getAllDonations() {
        return donationRepository.findAll()
                .stream()
                .map(donationMapper::toDto)
                .toList();
    }

    @Override
    public DonationResponseDto getDonationByPublicId(UUID publicId) {
        Donation donation = donationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Ce don n'existe pas"));
        return donationMapper.toDto(donation);
    }

    @Override
    public DonationResponseDto getDonationById(Long id) {
        Donation donation = donationRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable"));
        return donationMapper.toDto(donation);
    }

    @Override
    public List<BeneficiaryCountDto> countDonationsByBeneficiary() {
        return donationRepository.countDonationsByBeneficiary()
                .stream()
                .map(obj -> new BeneficiaryCountDto(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        obj[3].toString(), // Transforme enumerate n texte
                        (Long) obj[4]
                ))
                .toList();
    }

    @Override
    public List<DonationResponseDto> findByBeneficiaryId(Long beneficiaryId) {
        return donationRepository.findByBeneficiaryId(beneficiaryId)
                .stream()
                .map(donationMapper::toDto)
                .toList();
    }

    @Override
    public List<DonationCountByYearDto> countDonationsByYear() {
        return donationRepository.countDonationsByYear()
                .stream()
                .map(obj -> new DonationCountByYearDto(
                        (Integer) obj[0],
                        (Long) obj[1]
                ))
                .toList();
    }

    @Override
    public List<DonationResponseDto> getDonationsByMonth(int year, int month) {
        YearMonth yearMonth = YearMonth.of(year, month);

        LocalDate startDate = yearMonth.atDay(1);
        LocalDate endDate = yearMonth.atEndOfMonth();

        return donationRepository.findByDateDonationBetween(startDate, endDate)
                .stream()
                .map(donationMapper::toDto)
                .toList();
    }

    @Override
    public List<DonationResponseDto> getDonationsByYear(int year) {
        Year targetYear = Year.of(year);

        LocalDate startDate = targetYear.atDay(1);
        LocalDate endDate = targetYear.atDay(targetYear.length());

        return donationRepository.findByDateDonationBetween(startDate, endDate)
                .stream()
                .map(donationMapper::toDto)
                .toList();
    }

    @Override
    public DonationResponseDto updateVisibilityDonation(UUID publicId) {
        Donation donation = donationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable."));

        if (donation.getPublicStatus()){
            donation.setPublicStatus(false);
        }else{
            donation.setPublicStatus(true);
        }

        return donationMapper.toDto(donationRepository.save(donation));
    }

    @Override
    public DonationResponseDto updateClosureStatusDonation(UUID publicId) {
        Donation donation = donationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable."));

        donation.setClosure_status(true);

        return donationMapper.toDto(donationRepository.save(donation));
    }

    @Override
    public DonationResponseDto updateDonation(UUID publicId, DonationRequestDto dto, MultipartFile photoFile) throws IOException {

        if (dto.getTitle() == null || dto.getTitle().trim().isEmpty()) {
            throw new BadRequestException("Le titre est obligatoire.");
        }

        if (dto.getDescription() == null || dto.getDescription().trim().isEmpty()) {
            throw new BadRequestException("La description est obligatoire.");
        }

        Beneficiary beneficiary = beneficiaryRepository.findById(dto.getBeneficiaryId())
                .orElseThrow(() -> new ResourceNotFoundException("Bénéficiaire introuble"));

        // Vérification doublon Beneficiary + Title
        if (donationRepository.existsByBeneficiaryIdAndTitleAndPublicIdNot(
                beneficiary.getId(),
                dto.getTitle().trim(),
                publicId
        )) {
            throw new BadRequestException(
                    "Ce bénéficiaire est déjà associé à ce titre de don."
            );
        }

        Donation donation = donationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable."));


        donation.setTitle(dto.getTitle());
        donation.setDescription(dto.getDescription());
        donation.setDateDonation(dto.getDateDonation());
        donation.setBeneficiary(beneficiary);

        if (photoFile != null && !photoFile.isEmpty()) {

            // supprimer ancienne photo
            if (donation.getPhoto() != null && !donation.getPhoto().isBlank()) {
                fileStorageService.deleteFile(donation.getPhoto());
            }

            // utiliser FileStorageService
            String fileName = fileStorageService.saveFile(photoFile);
            donation.setPhoto(fileName);
        }

        return donationMapper.toDto(donationRepository.save(donation));
    }

    @Override
    public void deleteDonation(UUID publicId) {
        Donation donation = donationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable"));

        // supprimer ancienne photo
        if (donation.getPhoto() != null && !donation.getPhoto().isBlank()) {
            fileStorageService.deleteFile(donation.getPhoto());
        }

        donationRepository.delete(donation);
    }

}
