package eajc.group.apv.services;

import eajc.group.apv.dto.RegulationRequestDto;
import eajc.group.apv.dto.RegulationResponseDto;
import eajc.group.apv.entity.Regulation;
import eajc.group.apv.entity.User;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.RegulationMapper;
import eajc.group.apv.repository.RegulationRepository;
import eajc.group.apv.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class RegulationServiceImpl implements  RegulationService{

    private final RegulationRepository regulationRepository;
    private final RegulationMapper regulationMapper;
    private final UserRepository userRepository;

    public RegulationServiceImpl(RegulationRepository regulationRepository, RegulationMapper regulationMapper, UserRepository userRepository) {
        this.regulationRepository = regulationRepository;
        this.regulationMapper = regulationMapper;
        this.userRepository = userRepository;
    }

    @Override
    public RegulationResponseDto createRegulation(RegulationRequestDto dto, Long userId) {

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));


        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if (dto.getDescription() == null || dto.getDescription().trim().isEmpty()) {
            throw new BadRequestException("La description est obligatoire.");
        }

        if (regulationRepository.existsByNameIgnoreCase(dto.getName().trim())) {
            throw new BadRequestException("Ce nom existe déjà.");
        }

        Regulation regulation = regulationMapper.toEntity(dto, user);
        Regulation regulationSave = regulationRepository.save(regulation);
        return regulationMapper.toDto(regulationSave);
    }

    @Override
    public List<RegulationResponseDto> getAllRegulations() {
        return regulationRepository.findAll()
                .stream()
                .map(regulationMapper::toDto)
                .toList();
    }

    @Override
    public RegulationResponseDto getRegulationByPublicId(UUID publicId) {
        Regulation regulation = regulationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("La régulation n'existe pas"));
        return regulationMapper.toDto(regulation);
    }

    @Override
    public RegulationResponseDto updateRegulation(UUID publicId, RegulationRequestDto dto, Long userId) {

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if (dto.getDescription() == null || dto.getDescription().trim().isEmpty()) {
            throw new BadRequestException("La description est obligatoire.");
        }

        if (regulationRepository.existsByNameIgnoreCaseAndPublicIdNot(dto.getName().trim(), publicId)){
            throw new BadRequestException("Ce nom existe déjà.");
        }

        Regulation regulation = regulationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Régulation introuvable"));

        regulation.setName(dto.getName());
        regulation.setDescription(dto.getDescription());
        regulation.setUpdateAt(LocalDateTime.now());
        regulation.setUser(user);

        return regulationMapper.toDto(regulationRepository.save(regulation));
    }

    @Override
    public void deleteRegulation(UUID publicId) {
        Regulation regulation = regulationRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Régulation introuvable"));
        regulationRepository.delete(regulation);
    }

}
