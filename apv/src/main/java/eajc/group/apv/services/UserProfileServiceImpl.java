package eajc.group.apv.services;

import eajc.group.apv.dto.GenderCountDto;
import eajc.group.apv.dto.UserProfileReasonRemovalDto;
import eajc.group.apv.dto.UserProfileRequestDto;
import eajc.group.apv.dto.UserProfileResponseDto;
import eajc.group.apv.entity.UserProfile;
import eajc.group.apv.entity.User;
import eajc.group.apv.enums.Reason;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.UserProfileMapper;
import eajc.group.apv.repository.UserProfileRepository;
import eajc.group.apv.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Service
public class UserProfileServiceImpl implements UserProfileService {

    private final UserProfileRepository userProfileRepository;
    private final UserRepository userRepository;
    private final UserProfileMapper profileMapper;
    private final FileStorageService fileStorageService;

    public UserProfileServiceImpl(UserProfileRepository userProfileRepository, UserRepository userRepository, UserProfileMapper profileMapper, FileStorageService fileStorageService) {
        this.userProfileRepository = userProfileRepository;
        this.userRepository = userRepository;
        this.profileMapper = profileMapper;
        this.fileStorageService = fileStorageService;
    }

    @Override
    public UserProfileResponseDto createProfile(UserProfileRequestDto profileDto, MultipartFile photoFile) throws IOException {
        User user = this.userRepository.findById(profileDto.getUserId())
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        String fileName = fileStorageService.saveFile(photoFile);

        UserProfile client = this.profileMapper.toEntity(profileDto, user, fileName);
        UserProfile clientSave = this.userProfileRepository.save(client);

        return profileMapper.toDto(clientSave);

    }

    @Override
    public List<UserProfileResponseDto> getAllProfiles() {
        return userProfileRepository.findAll()
                .stream()
                .map(profileMapper::toDto)
                .toList();
    }

    @Override
    public UserProfileResponseDto getProfileByPublicId(UUID publicId) {
        UserProfile profile = userProfileRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Profil introuvable"));

        return profileMapper.toDto(profile);
    }

    @Override
    public UserProfileResponseDto getProfileByUser(UUID publicId) {
        User user = this.userRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        UserProfile client = userProfileRepository.findByUser(user);

        return profileMapper.toDto(client);
    }

    @Override
    public List<UserProfileResponseDto> getTodayRegistrations() {
        return userProfileRepository.findByRegistrationDate(LocalDate.now())
                .stream()
                .map(profileMapper::toDto)
                .toList();
    }

    @Override
    public List<GenderCountDto> countProfilesByGender() {
        return userProfileRepository.countProfilesByGender()
                .stream()
                .map(obj -> new GenderCountDto(
                        obj[0].toString(),
                        (Long) obj[1]
                ))
                .toList();
    }

    @Override
    public List<UserProfileResponseDto> getProfilesByReasonRemovalNot() {
        return userProfileRepository.findByReasonRemovalNot(Reason.JE_SUIS_INTERESSE)
                .stream()
                .map(profileMapper::toDto)
                .toList();
    }

    @Override
    public UserProfileResponseDto updateReasonRemoval(UUID publicId, UserProfileReasonRemovalDto dto) {
        UserProfile profile = userProfileRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Profil introuvable"));

        profile.setReasonRemoval(dto.getReasonRemoval());
        return profileMapper.toDto(userProfileRepository.save(profile));
    }

    @Override
    public UserProfileResponseDto updateProfile(UUID publicId, UserProfileRequestDto dto) {
        UserProfile profile = userProfileRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Profil introuvable"));

        User user = userRepository.findById(dto.getUserId())
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        profile.setLastName(dto.getLastName());
        profile.setFirstName(dto.getFirstName());
        profile.setGender(dto.getGender());
        profile.setPhone(dto.getPhone());
        profile.setAddress(dto.getAddress());
        profile.setCountry(dto.getCountry());
        profile.setCity(dto.getCity());
        profile.setBorough(dto.getBorough());
        profile.setProfession(dto.getProfession());
        profile.setUser(user);

        return profileMapper.toDto(userProfileRepository.save(profile));
    }

    @Override
    public UserProfileResponseDto updatePhotoProfile(UUID publicId, MultipartFile photoFile) throws IOException {

        UserProfile profile = userProfileRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Profil introuvable"));

        if (photoFile != null && !photoFile.isEmpty()) {

            // supprimer ancien logo
            if (profile.getPhoto() != null && !profile.getPhoto().isBlank()) {
                fileStorageService.deleteFile(profile.getPhoto());
            }

            // utiliser FileStorageService
            String fileName = fileStorageService.saveFile(photoFile);
            profile.setPhoto(fileName);
        }

        UserProfile updated = userProfileRepository.save(profile);

        return profileMapper.toDto(userProfileRepository.save(updated));
    }

    @Override
    public void deleteProfile(UUID publicId) {
        UserProfile profile = userProfileRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Profile introuvable"));

        // supprimer ancien logo
        if (profile.getPhoto() != null && !profile.getPhoto().isBlank()) {
            fileStorageService.deleteFile(profile.getPhoto());
        }

        userProfileRepository.delete(profile);
    }


}
