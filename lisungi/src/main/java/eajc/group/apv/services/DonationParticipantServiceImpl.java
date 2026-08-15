package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import eajc.group.apv.entity.DonationParticipant;
import eajc.group.apv.entity.Donation;
import eajc.group.apv.entity.User;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.DonationParticipantMapper;
import eajc.group.apv.repository.*;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class DonationParticipantServiceImpl implements DonationParticipantService{

    private final DonationParticipantRepository donationParticipantRepository;
    private final DonationParticipantMapper donationParticipantMapper;
    private final UserRepository userRepository;
    private final DonationRepository donationRepository;

    public DonationParticipantServiceImpl(DonationParticipantRepository donationParticipantRepository, DonationParticipantMapper donationParticipantMapper, UserRepository userRepository, DonationRepository donationRepository) {
        this.donationParticipantRepository = donationParticipantRepository;
        this.donationParticipantMapper = donationParticipantMapper;
        this.userRepository = userRepository;
        this.donationRepository = donationRepository;
    }


    @Override
    public DonationParticipantResponseDto createDonationParticipant(DonationParticipantRequestDto dto, Long userId) {

        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if ((dto.getDescription() == null && dto.getAmount() == null) || (dto.getDescription().trim().isEmpty() && dto.getAmount() == null)) {
            throw new BadRequestException("Au moins l’un des deux champs, Montant ou Description, doit être renseigné.");
        }

        // Vérification doublon particpant + don
        if (donationParticipantRepository.existsByDonationIdAndName(
                dto.getDonationId(),
                dto.getName()
        )) {
            throw new BadRequestException(
                    "Ce participant a déjà contribué pour ce don."
            );
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        Donation donation = donationRepository.findById(dto.getDonationId())
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable"));

        if (donation.getClosure_status()){
            throw new BadRequestException("Ce don a déjà été clôturé.");
        }

        DonationParticipant donationParticipant = donationParticipantMapper.toEntity(dto, donation, user);
        DonationParticipant donationParticipantSave = donationParticipantRepository.save(donationParticipant);
        return donationParticipantMapper.toDto(donationParticipantSave);
    }

    @Override
    public List<DonationParticipantResponseDto> getAllDonationParticipants() {
        return donationParticipantRepository.findAll()
                .stream()
                .map(donationParticipantMapper::toDto)
                .toList();
    }

    @Override
    public DonationParticipantResponseDto getDonationParticipantByPublicId(UUID publicId) {
        DonationParticipant donationParticipant = donationParticipantRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contribution not found"));
        return donationParticipantMapper.toDto(donationParticipant);
    }

    @Override
    public List<ParticipantsByDonationCountDto> countParticipantsByDonationAndBeneficiary(UUID beneficiaryPublicId) {
        return donationParticipantRepository.countParticipantsByDonationAndBeneficiary(beneficiaryPublicId)
                .stream()
                .map(obj -> new ParticipantsByDonationCountDto(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        (Boolean) obj[3],
                        (Long) obj[4]
                ))
                .toList();
    }


    @Override
    public DonationParticipantResponseDto updateDonationParticipant(UUID publicId, DonationParticipantRequestDto dto, Long userId) {

        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if ((dto.getDescription() == null && dto.getAmount() == null) || (dto.getDescription().trim().isEmpty() && dto.getAmount() == null)) {
            throw new BadRequestException("Au moins l’un des deux champs, Montant ou Description, doit être renseigné.");
        }

        // Vérification doublon particpant + don
        if (donationParticipantRepository.existsByDonationIdAndNameAndPublicIdNot(
                dto.getDonationId(),
                dto.getName(),
                publicId
        )) {
            throw new BadRequestException(
                    "Ce participant a déjà contribué pour ce don."
            );
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        Donation donation = donationRepository.findById(dto.getDonationId())
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable"));

        DonationParticipant donationParticipant = donationParticipantRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Participant introuvable"));

        if (donation.getClosure_status()){
            throw new BadRequestException("Ce don a déjà été clôturé.");
        }

        donationParticipant.setName(dto.getName());
        donationParticipant.setDescription(dto.getDescription());
        donationParticipant.setItemType(dto.getItemType());
        donationParticipant.setAmount(dto.getAmount());
        donationParticipant.setDonation(donation);
        donationParticipant.setUser(user);

        return donationParticipantMapper.toDto(donationParticipantRepository.save(donationParticipant));
    }

    @Override
    public List<BeneficiaryDonationParticipantCountDto> countDonationByBeneficiaryWithParticipant() {
        return donationParticipantRepository.countDonationByBeneficiaryWithParticipant()
                .stream()
                .map(obj -> new BeneficiaryDonationParticipantCountDto(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        (Long) obj[3]
                ))
                .toList();
    }

    @Override
    public List<DonationParticipantResponseDto> getParticipantsByDonation(UUID donationPublicId) {
        Donation donation = donationRepository.findByPublicId(donationPublicId)
                .orElseThrow(() -> new ResourceNotFoundException("Don introuvable"));

        return donationParticipantRepository.findByDonationId(donation.getId())
                .stream()
                .map(donationParticipantMapper::toDto)
                .toList();
    }

    @Override
    public void deleteDonationParticipant(UUID publicId) {
        DonationParticipant donationParticipant = donationParticipantRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Participant introuvable"));

        donationParticipantRepository.delete(donationParticipant);
    }

}
