package eajc.group.apv.services;

import eajc.group.apv.dto.BeneficiaryRequestDto;
import eajc.group.apv.dto.BeneficiaryResponseDto;
import eajc.group.apv.entity.Beneficiary;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.BeneficiaryMapper;
import eajc.group.apv.repository.BeneficiaryRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class BeneficiaryServiceImpl implements BeneficiaryService{

    private final BeneficiaryRepository beneficiaryRepository;
    private final BeneficiaryMapper beneficiaryMapper;

    public BeneficiaryServiceImpl(BeneficiaryRepository beneficiaryRepository, BeneficiaryMapper beneficiaryMapper) {
        this.beneficiaryRepository = beneficiaryRepository;
        this.beneficiaryMapper = beneficiaryMapper;
    }


    @Override
    public BeneficiaryResponseDto createBeneficiary(BeneficiaryRequestDto dto) {
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if (dto.getCountry() == null || dto.getCountry().trim().isEmpty()) {
            throw new BadRequestException("Le pays est obligatoire.");
        }

        if (dto.getCity() == null || dto.getCity().trim().isEmpty()) {
            throw new BadRequestException("La ville is empty.");
        }

        if (dto.getBorough() == null || dto.getBorough().trim().isEmpty()) {
            throw new BadRequestException("La zone est obligatoire.");
        }

        if ((dto.getPhone() == null && dto.getEmail() == null) || (dto.getPhone().trim().isEmpty() && dto.getEmail().trim().isEmpty())){
            throw new BadRequestException("Le téléphone ou l'email est obligatoire.");
        }

        if (beneficiaryRepository.existsByPhoneAndNameIgnoreCase(dto.getPhone().trim(), dto.getName().trim())) {
            throw new BadRequestException("Un bénéficiaire avec le même nom et même numéro de téléphone existe déjà.");
        }

        Beneficiary beneficiary = beneficiaryMapper.toEntity(dto);
        Beneficiary beneficiarySave = beneficiaryRepository.save(beneficiary);
        return beneficiaryMapper.toDto(beneficiarySave);
    }

    @Override
    public List<BeneficiaryResponseDto> getAllBeneficiaries() {
        return beneficiaryRepository.findAll()
                .stream()
                .map(beneficiaryMapper::toDto)
                .toList();
    }

    @Override
    public BeneficiaryResponseDto getBeneficiaryByPublicId(UUID publicId) {
        Beneficiary beneficiary = beneficiaryRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Bénéficiaire introuvable"));
        return beneficiaryMapper.toDto(beneficiary);
    }

    @Override
    public BeneficiaryResponseDto updateBeneficiary(UUID publicId, BeneficiaryRequestDto dto) {
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if (dto.getCountry() == null || dto.getCountry().trim().isEmpty()) {
            throw new BadRequestException("Le pays est obligatoire.");
        }

        if (dto.getCity() == null || dto.getCity().trim().isEmpty()) {
            throw new BadRequestException("La ville is empty.");
        }

        if (dto.getBorough() == null || dto.getBorough().trim().isEmpty()) {
            throw new BadRequestException("La zone est obligatoire.");
        }

        if ((dto.getPhone() == null && dto.getEmail() == null) || (dto.getPhone().trim().isEmpty() && dto.getEmail().trim().isEmpty())){
            throw new BadRequestException("Le téléphone ou l'email est obligatoire.");
        }

        if (beneficiaryRepository.existsByPhoneAndNameIgnoreCaseAndPublicIdNot(dto.getPhone().trim(), dto.getName().trim(), publicId)) {
            throw new BadRequestException("Un bénéficiaire avec le même nom et même numéro de téléphone existe déjà.");
        }

        Beneficiary beneficiary = beneficiaryRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Bénéficiaire introuvable"));

        beneficiary.setType(dto.getType());
        beneficiary.setName(dto.getName());
        beneficiary.setCountry(dto.getCountry());
        beneficiary.setCity(dto.getCity());
        beneficiary.setBorough(dto.getBorough());
        beneficiary.setAddress(dto.getAddress());
        beneficiary.setPhone(dto.getPhone());
        beneficiary.setEmail(dto.getEmail());
        beneficiary.setDateExistence(dto.getDateExistence());
        return beneficiaryMapper.toDto(beneficiaryRepository.save(beneficiary));
    }

    @Override
    public void deleteBeneficiary(UUID publicId) {
        Beneficiary beneficiary = beneficiaryRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Bénéficiaire introuvable"));
        beneficiaryRepository.delete(beneficiary);
    }

}
